import streamlit as st
import mediapipe as mp
import numpy as np
import cv2
import time
import tempfile
from PIL import Image
import io

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

DEMO_IMAGE = './content/demo.jpg'
DEMO_VIDEO = './content/demo.mp4'

st.title("Face Mesh with MediaPipe")

st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child{
        width: 350px;
    }
    [data-testid="stSidebar"][aria-expanded="false] > div:first-child{
        width: 350px;
        margin-left: -350px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.title('Facemesh Sidebar')
st.sidebar.subheader('Parameters')


## Caching
@st.cache()
## Two Cases: Images and Videos
def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image

    if width is None:
        #r = width / float(w)
        r = height / float(h)
        dim = (int(w * r), height)

    else:
        r = width / float(w)
        dim = (width, int(h * r))

    ## Resize Image
    resized = cv2.resize(image, dim, interpolation=inter)

    return resized


## Various Application States
app_mode = st.sidebar.selectbox('Choose the App Mode',
                                ['About App', 'Run on Image', 'Run on Video']
                                )

if app_mode == 'About App':
    st.markdown("An application of Machine Learning to determine the Human Face in a served image, "
                "modeled on the MediaPipe infrastructure, method is fast and computational cheap. "
                "\n\n"
                "To use the app, follow the sidebar and enter an image of choice and play around."
                "\n\n\n"
                "Project is heavily influenced by the work of [Ritesh Kanjee|Augmented StartUps](https://www.augmentedstartups.com/)")
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child{
            width: 350px;
        }
        [data-testid="stSidebar"][aria-expanded="false] > div:first-child{
            width: 350px;
            margin-left: -350px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.video(DEMO_VIDEO)

    # st.markdown('''
    # #   About Me \n
    #     **Pattern** | **Recognition**
    # ''')

elif app_mode == 'Run on Image':
    st.sidebar.markdown('---')
    contour_value_1 = st.sidebar.slider('Contour Thickness',
                                        min_value=1, max_value=3, value=1)
    contour_value_2 = st.sidebar.slider('Circle Radius',
                                        min_value=0, max_value=3, value=1)
    drawing_spec = mp_drawing.DrawingSpec(thickness=contour_value_1, circle_radius=contour_value_2)

    st.markdown(
        """
        <style>
        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child{
            width: 350px;
        }
        [data-testid="stSidebar"][aria-expanded="false] > div:first-child{
            width: 350px;
            margin-left: -350px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("**Detected Faces**")
    kpi1_text = st.markdown("0")

    st.sidebar.markdown('---')
    max_faces = st.sidebar.number_input('Maximum Number of Face',
                                        value=2, min_value=1)

    st.sidebar.markdown('---')  ## Divider
    detection_confidence = st.sidebar.slider('Min Detection Confidence', min_value=0.0, max_value=1.0,
                                             value=0.5)  ## Sensitivity
    st.sidebar.markdown('---')

    img_file_buffer = st.sidebar.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
    if img_file_buffer is not None:
        image = np.array(Image.open(img_file_buffer))
    else: #default to demo image
        demo_image = DEMO_IMAGE
        image = np.array(Image.open(demo_image))

    st.sidebar.text("Placed Image")
    st.sidebar.image(image)
    face_count = 0

    # Dashboard
    with mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=max_faces,
        min_detection_confidence=detection_confidence
    ) as face_mesh:
        results = face_mesh.process(image)
        out_image = image.copy()

        ## Face Landmark Drawing
        for face_landmarks in results.multi_face_landmarks:
            face_count += 1

            if face_count > 0:
                mp_drawing.draw_landmarks(
                    image=out_image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=drawing_spec,
                    connection_drawing_spec=drawing_spec
                )

                kpi1_text.write(f"<h1 style='text-align: center; color:red;'>{face_count}</h1>", unsafe_allow_html=True)
            else:
                kpi1_text.write(f"<h1 style='text-align: center; color:green;'>Place an image with faces</h1>",
                                unsafe_allow_html=True)

        st.subheader('Output Image')
        st.image(out_image, use_column_width=True)

        ## Save Result
        # if st.button("Download a copy"):

        output = io.BytesIO()
        output_image = Image.fromarray(out_image) ## convert result from np.ndarray
        output_image.save(output, format='JPEG') ## save again
        result_image = output.getvalue()


        btn = st.download_button(
            label="Keep a copy",
            data=result_image,
            file_name="meshed_image.png",
            mime="image/jpeg")

elif app_mode == 'Run on Video':
    # st.set_option('deprecation.showfileUploaderEncoding', False)
    #
    # use_webcam = st.sidebar.button('Use Webcam')
    # record = st.sidebar.checkbox('Record Video')
    #
    # if record:
    #     st.checkbox("Recording", value=True)
    #
    # st.markdown(
    #     """
    #     <style>
    #     [data-testid="stSidebar"][aria-expanded="true"] > div:first-child{
    #         width: 350px;
    #     }
    #     [data-testid="stSidebar"][aria-expanded="false] > div:first-child{
    #         width: 350px;
    #         margin-left: -350px;
    #     }
    #     </style>
    #     """,
    #     unsafe_allow_html=True,
    # )
    #
    # max_faces = st.sidebar.number_input('Maximum Number of Face', value=5, min_value=1)
    #
    # st.sidebar.markdown('---')
    # detection_confidence = st.sidebar.slider('Min Detection Confidence', min_value=0.0, max_value=1.0,
    #                                          value=0.5)  ## Sensitivity
    # tracking_confidence = st.sidebar.slider('Min Tracking Confidence', min_value=0.0, max_value=1.0, value=0.5)
    # st.sidebar.markdown('---')
    #
    # st.markdown(" ## Output")
    #
    # stframe = st.empty()
    # video_file_buffer = st.sidebar.file_uploader("Upload Video", type=["mp4", "mov",'avi','asf','m4v'])
    # tffile = tempfile.NamedTemporaryFile(delete=False)
    #
    # if not video_file_buffer:
    #     if use_webcam:
    #         vid = cv2.VideoCapture(0)
    #     else:
    #         vid = cv2.VideoCapture(DEMO_VIDEO)
    # else:
    #     tffile.write(video_file_buffer.read())
    #     vid = cv2.VideoCapture(tffile.name)
    #
    # width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    # height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # fps_input = int(vid.get(cv2.CAP_PROP_FPS))
    #
    # ##Recording
    # # codec = cv2.VideoWriter_fourcc('V', 'P', '0', '9')
    # codec = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    # out = cv2.VideoWriter('output1.mp4', codec, fps_input, (width, height))
    #
    # st.sidebar.text('Input Video')
    # st.sidebar.video(tffile.name)
    #
    # fps = 0
    # i = 0
    # drawing_spec = mp_drawing.DrawingSpec(thickness=2, circle_radius=1)
    #
    # kpi1, kpi2, kpi3 = st.columns(3)
    #
    # with kpi1:
    #     st.markdown("**Frame Rate**")
    #     kpi1_text = st.markdown("0")
    #
    # with kpi2:
    #     st.markdown("**Detected Faces**")
    #     kpi2_text = st.markdown("0")
    #
    # with kpi3:
    #     st.markdown("**Image Width**")
    #     kpi3_text = st.markdown("0")
    #
    # st.markdown("<hr/>", unsafe_allow_html=True)
    #
    # ##Dashboard
    # with mp_face_mesh.FaceMesh(
    #     max_num_faces=max_faces,
    #     min_detection_confidence=detection_confidence,
    #     min_tracking_confidence=tracking_confidence
    # ) as face_mesh:
    #     prevTime = 0
    #
    #     while vid.isOpened():
    #         i += 1
    #         ret, frame = vid.read()
    #         if not ret:
    #             continue
    #         results = face_mesh.process(frame)
    #         frame.flags.writeable = True
    #
    #         face_count = 0
    #         if results.multi_face_landmarks:
    #             for face_landmarks in results.multi_face_landmarks:
    #                 face_count += 1
    #                 mp_drawing.draw_landmarks(
    #                     image=frame,
    #                     landmark_list=face_landmarks,
    #                     connections=mp_face_mesh.FACEMESH_CONTOURS,
    #                     landmark_drawing_spec=drawing_spec,
    #                     connection_drawing_spec=drawing_spec
    #                 )
    #
    #     currTime = time.time()
    #     fps = 1 / (currTime - prevTime)
    #     prevTime = currTime
    #
    #     if record:
    #         out.write(frame)
    #
    #     ##Output Dashboard
    #     kpi1_text.write(f"<h1 style='text-align: center; color:red;'>{int(fps)}</h1>", unsafe_allow_html=True)
    #     kpi2_text.write(f"<h1 style='text-align: center; color:red;'>{face_count}</h1>", unsafe_allow_html=True)
    #     kpi3_text.write(f"<h1 style='text-align: center; color:red;'>{width}</h1>", unsafe_allow_html=True)
    #
    #     frame = cv2.resize(frame, (0, 0), fx=0.8, fy=0.8)
    #     frame = image_resize(image=frame, width=640)
    #     stframe.image(frame, channels='BGR', use_column_width=True)
    #
    # st.text('Video Processed')
    #
    # output_video = open('output1.mp4','rb')
    # out_bytes = output_video.read()
    # st.video(out_bytes)
    #
    # vid.release()
    # out. release()

    st.write("⛏ Work in progress. \n Bear with Author.")
