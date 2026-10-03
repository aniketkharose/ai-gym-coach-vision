import streamlit as st
import os
import time
import pandas as pd
from dotenv import load_dotenv
from services.auth.login_wall import render_login_wall
from services.state.session_defaults import initial_session_defaults
from services.config.workout_config import EXERCISE_OPTIONS
from services.ui.style_loader import load_css, inject_local_font, inject_webrtc_styles
from services.ui import components as ui
from services.persistence.exercise_repository import init_db
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from twilio.rest import Client
from services.vision.exercise_video_processor import VideoProcessorClass
from services.tracking.metrics import sync_metrics_update
from services.persistence.exercise_repository import get_users_exercises
from groq import Groq
from services.coaching.llm import LLMCoach
from services.coaching.tts import TextToSpeech
from services.coaching.voice_pipeline import VoicePipeline, autoplay_audio


@st.cache_data(ttl=300)
def get_ice_servers():
    try:
        account_sid = st.secrets["TWILIO_ACCOUNT_SID"]
        auth_token = st.secrets["TWILIO_AUTH_TOKEN"]
    except Exception:
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")

    if not account_sid or not auth_token:
        st.error("Twilio credentials are missing.")
        return []

    try:
        client = Client(account_sid, auth_token)
        token = client.tokens.create()
        return token.ice_servers
    except Exception as e:
        st.error(f"Twilio ICE server error: {e}")
        return []


def get_exercise_metrics(exercise):
    """Returns (section title, [(label, value), ...]) for the current exercise."""
    s = st.session_state
    if exercise == "Squats":
        return "Squat Metrics", [
            ("Knee Angle", f"{s.knee_angle}°"),
            ("Back Angle", f"{s.back_angle}°"),
            ("Depth Status", s.depth_status),
        ]
    if exercise == "Push-ups":
        return "Push-up Metrics", [
            ("Elbow Angle", f"{s.elbow_angle}°"),
            ("Body Alignment", s.body_alignment),
            ("Hip Position", s.hip_status),
        ]
    if exercise == "Biceps Curls (Dumbbell)":
        return "Curl Metrics", [
            ("Elbow Angle", f"{s.elbow_angle}°"),
            ("Shoulder Stability", s.shoulder_status),
            ("Swing Detection", s.swing_status),
        ]
    if exercise == "Shoulder Press":
        return "Shoulder Press Metrics", [
            ("Elbow Angle", f"{s.elbow_angle}°"),
            ("Arm Extension", s.extension_status),
            ("Back Arch", s.back_arch_status),
        ]
    if exercise == "Lunges":
        return "Lunge Metrics", [
            ("Front Knee Angle", f"{s.front_knee_angle}°"),
            ("Torso Angle", f"{s.torso_angle}°"),
            ("Balance Status", s.balance_status),
        ]
    return None, []


def main():
    st.set_page_config(
        page_icon="🏋️‍♀️",
        page_title="AI Real-time GYM Coach",
        initial_sidebar_state="expanded",
        layout="centered"
    )

    load_dotenv()

    load_css(os.path.join(os.getcwd(), "static", "style.css"))
    inject_local_font(os.path.join(os.getcwd(), "static", "AdobeClean.otf"), "AdobeClean")

    init_db()

    if not render_login_wall():
        return

    initial_session_defaults()

    if "voice_pipeline" not in st.session_state:
        try:
            api_key = os.environ.get("GROQ_API_KEY", "")

            if not api_key:
                raise ValueError("GROQ_API_KEY not found in .env file.")

            groq_client = Groq(api_key=api_key)
            llm_coach = LLMCoach(groq_client)
            tts = TextToSpeech()

            st.session_state.voice_pipeline = VoicePipeline(llm_coach, tts)

        except Exception as e:
            st.session_state.voice_pipeline = None
            st.error(f"Voice pipeline error: {e}")

    workout_started = st.session_state.get("workout_started", False)

    # ------------------------------------------------------------------ SIDEBAR
    with st.sidebar:
        ui.brand(st.session_state.get("username"))
        ui.section_label("Workout Plan")

        if not workout_started:
            plan_exercise = st.selectbox("Exercise", options=EXERCISE_OPTIONS, key="plan_exercise")
            plan_sets = st.number_input("Sets", min_value=0, max_value=50, key="plan_sets", step=1)
            plan_reps = st.number_input("Reps per Set", min_value=0, max_value=50, key="plan_reps", step=1)

            st.markdown("")

            start_session_button = st.button("Start Workout", width="stretch", key="start_session_button")

            if start_session_button:
                st.session_state.exercise_type = plan_exercise
                st.session_state.target_sets = int(plan_sets)
                st.session_state.reps_per_set = int(plan_reps)
                st.session_state.reps = 0
                st.session_state.workout_started = True
                st.session_state.set_cycle_started_at = time.time()
                st.session_state.last_saved_sets_completed = 0

                if st.session_state.voice_pipeline:
                    result = st.session_state.voice_pipeline.process_event(
                        event="workout_started",
                        exercise=plan_exercise,
                        metrics={}
                    )
                    if result:
                        st.session_state.audio_to_play, st.session_state.coach_feedback = result

                st.session_state.last_notified_sets_completed = 0
                st.session_state.last_notified_workout_complete = False
                st.rerun()
        else:
            exercise = st.session_state.get("exercise_type")
            sets = st.session_state.get("target_sets")
            reps = st.session_state.get("reps_per_set")

            ui.plan_chip(exercise, sets, reps)

            end_session_button = st.button("End Workout", key="end_session_button", width="stretch")

            if end_session_button:
                st.session_state.workout_started = False

                if st.session_state.voice_pipeline:
                    result = st.session_state.voice_pipeline.process_event(
                        event="workout_completed",
                        exercise=exercise,
                        metrics={}
                    )
                    if result:
                        st.session_state.audio_to_play, st.session_state.coach_feedback = result

                st.rerun()

        if workout_started:
            exercise = st.session_state.get("exercise_type")

            ui.section_label("Progress")
            ui.stat_cards([("Total Reps", st.session_state.get("reps", 0))])
            ui.progress_rings(
                st.session_state.get("current_set_reps", 0),
                st.session_state.get("reps_per_set", 0),
                st.session_state.get("sets_completed", 0),
                st.session_state.get("target_sets", 0),
            )

            title, items = get_exercise_metrics(exercise)
            if items:
                ui.section_label(title)
                ui.stat_cards(items)

    # --------------------------------------------------------------------- MAIN
    ui.hero(
        "AI Real-time Gym Coach",
        "Real-time pose detection with proactive AI voice coaching",
        live=workout_started,
    )

    if st.session_state.get("audio_to_play"):
        autoplay_audio(st.session_state.audio_to_play)

    if st.session_state.get("coach_feedback"):
        ui.coach_bubble(st.session_state.coach_feedback)

    if not workout_started:
        ui.empty_state()
    else:
        ice_servers = get_ice_servers()
        context = webrtc_streamer(
            key="exercise-analysis",
            mode=WebRtcMode.SENDRECV,
            video_processor_factory=VideoProcessorClass,
            rtc_configuration={"iceServers": ice_servers},
            media_stream_constraints={"video": True, "audio": False},
            async_processing=True
        )

        sync_metrics_update(context)

        if context.state.playing:
            time.sleep(0.25)
            st.rerun()

        inject_webrtc_styles()

    st.divider()

    ui.section_label("Workout History")

    user_id = st.session_state.get("user_id", 0)

    if isinstance(user_id, int):
        history_rows = get_users_exercises(user_id)

        arr = [
            {
                "Exercise": row['exercise_name'],
                "Reps": row['reps'],
                "Sets": row['sets'],
                "Time (sec)": row['time'],
                "Date": row['created_at']
            }
            for row in history_rows
        ]

        df = pd.DataFrame(arr)

        if not df.empty:
            df["Date"] = pd.to_datetime(df["Date"]).dt.date

            ui.kpi_grid([
                (int(df["Reps"].sum()), "Total reps"),
                (int(df["Sets"].sum()), "Total sets"),
                (f"{df['Time (sec)'].sum() / 60:.0f}m", "Time trained"),
                (df["Date"].nunique(), "Active days"),
            ])

            st.bar_chart(df.groupby("Date")["Reps"].sum(), color="#C6FF3D", height=220)

            agg_df = df.groupby(["Exercise", "Date"]).agg({
                "Reps": "sum",
                "Sets": "sum",
                "Time (sec)": "sum"
            }).reset_index()
            st.dataframe(agg_df, width="stretch", hide_index=True)
        else:
            st.info("No workout history yet. Start your first workout! 💪")


if __name__ == "__main__":
    main()