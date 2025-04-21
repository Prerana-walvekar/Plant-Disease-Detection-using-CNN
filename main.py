# 📦 Library imports
import numpy as np
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# ✅ Load the model (224x224 MobileNetV2)
model = load_model('mobilenetv2_plant_model.h5')

# 🏷️ Updated class names (11 classes)
CLASS_NAMES = [
    'Corn___Cercospora_leaf_spot_Gray_leaf_spot',
    'Corn___Common_rust',
    'Corn___Northern_Leaf_Blight',
    'Corn___healthy',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Tomato___Bacterial_spot',
    'Tomato___Early_blight',
    'Tomato___Late_blight',
    'Tomato___healthy'
]

# 🛡️ Prevention strategies for each class
PREVENTION = {
    'Corn___Cercospora_leaf_spot_Gray_leaf_spot': """- Plant resistant hybrids if available.\n- Rotate crops with non-hosts like soybeans.\n- Remove and destroy crop debris.\n- Apply fungicides during early tasseling if needed.""",
    'Corn___Common_rust': """- Use resistant corn hybrids.\n- Ensure proper spacing for airflow.\n- Apply fungicides if rust appears before silking.""",
    'Corn___Northern_Leaf_Blight': """- Choose resistant hybrids.\n- Rotate with non-host crops.\n- Bury crop residues through tillage.\n- Use fungicides at VT/R1 if pressure is high.""",
    'Corn___healthy': """- No disease detected.\n- Maintain regular crop monitoring.\n- Use balanced nutrients and good irrigation practices.""",
    'Potato___Early_blight': """- Use certified disease-free seeds.\n- Rotate with non-solanaceous crops.\n- Remove and destroy infected debris.\n- Apply protectant fungicides like chlorothalonil early in season.""",
    'Potato___Late_blight': """- Avoid overhead irrigation.\n- Grow blight-resistant varieties.\n- Monitor during cool, moist weather.\n- Use fungicides like metalaxyl or cyazofamid.""",
    'Potato___healthy': """- Leaf appears healthy.\n- Continue monitoring for signs of blight.\n- Maintain good hilling and sanitation practices.""",
    'Tomato___Bacterial_spot': """- Use certified disease-free seeds or transplants.\n- Avoid working with wet plants.\n- Apply copper-based bactericides preventatively.\n- Rotate with non-solanaceous crops.""",
    'Tomato___Early_blight': """- Remove lower infected leaves.\n- Use resistant varieties.\n- Practice 2–3 year crop rotation.\n- Apply fungicides like mancozeb or chlorothalonil.""",
    'Tomato___Late_blight': """- Increase plant spacing for airflow.\n- Avoid overhead watering.\n- Use resistant cultivars.\n- Apply fungicides like cyazofamid during cool, wet conditions.""",
    'Tomato___healthy': """- Leaf is healthy.\n- Maintain good irrigation and spacing.\n- Keep monitoring for any disease symptoms."""

}

if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("You must be logged in to access this page.")
    switch_page("login1")  # change "login" to the correct name of your login/signup page
else:

    # 🌿 Streamlit setup
    st.set_page_config(page_title="Plant Disease Detection", layout="centered")
    st.title("🌿 Plant Disease Detection")
    st.markdown("Upload an image of a plant leaf to detect disease and receive prevention tips.")

    # 📤 Upload image
    plant_image = st.file_uploader("Choose a leaf image...", type=["jpg", "jpeg", "png"])
    submit = st.button('Predict Disease')

    if submit:
        if plant_image is not None:
            # Decode image
            file_bytes = np.asarray(bytearray(plant_image.read()), dtype=np.uint8)
            opencv_image = cv2.imdecode(file_bytes, 1)

            # Display resized image
            display_image = cv2.resize(opencv_image, (300, 300))
            st.image(display_image, channels="BGR", caption="Uploaded Leaf Image")

            # Preprocess for MobileNetV2
            model_input = cv2.resize(opencv_image, (224, 224))
            model_input = preprocess_input(model_input)
            model_input = np.expand_dims(model_input, axis=0)

            # Prediction
            Y_pred = model.predict(model_input)
            prediction = CLASS_NAMES[np.argmax(Y_pred)]

            # Output
            st.success(f"🩺 Predicted: **{prediction.replace('___', ' → ').replace('_', ' ')}**")
            st.markdown("### 🛡️ Prevention Tips")
            st.markdown(PREVENTION[prediction])
        else:
            st.warning("Please upload an image first.")
