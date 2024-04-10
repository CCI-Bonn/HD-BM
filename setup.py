from setuptools import setup


setup(
    name="hd_bm",
    version="1.0",
    packages=["hd_bm"],
    description="Tool for automated segmentation of brain metastasis. "
    "This is the result of a joint project between the Department of Neuroradiology at the"
    " Heidelberg University Hospital and the Division of Medical Image Computing at "
    "the German Cancer Research Center (DKFZ). See readme.md for more information",
    url="https://github.com/NeuroAI-HD/HD-BM",
    python_requires=">=3.6",
    author="Tassilo Wald",
    author_email="tassilo.wald@dkfz-heidelberg.de",
    license="Apache 2.0",
    zip_safe=False,
    install_requires=[
        "nnunet @ git+https://github.com/MIC-DKFZ/nnUNet.git@v1.7.1",
        "matplotlib",
        "SimpleITK<2.1.0 ; python_version<='3.6'",
        "SimpleITK>=2.2.1 ; python_version>'3.6'",
    ],
    extras_require={
        ':python_version=="3.6"': ["torch==1.10.2", "batchgenerators==0.25"],
        ':python_version=="3.7"': ["importlib_metadata", "torch==1.10.2", "batchgenerators==0.25"],
        ':python_version=="3.8"': ["importlib_metadata", "torch", "batchgenerators==0.25"],
        ':python_version=="3.9"': ["torch==2.2.2", "batchgenerators==0.25"],
        ':python_version=="3.10"': ["torch", "batchgenerators==0.25"],
        ':python_version=="3.11"': ["torch", "batchgenerators==0.25"],
        ':python_version=="3.12"': ["torch", "batchgenerators==0.25"],
    },
    entry_points={
        "console_scripts": [
            "hd_bm_evaluate = hd_bm.evaluate:main",
            "hd_bm_predict = hd_bm.hd_bm_predict:main",
            "hd_bm_predict_folder = hd_bm.hd_bm_predict_folder:main",
            "hd_bm_predict_folder_with_labels = hd_bm.hd_bm_predict_folder_with_labels:main",
            "hd_bm_slim_predict =  hd_bm.hd_bm_slim_predict:main",
            "hd_bm_slim_predict_folder = hd_bm.hd_bm_slim_predict_folder:main",
            "hd_bm_slim_predict_folder_with_labels = hd_bm.hd_bm_slim_predict_folder_with_labels:main",
        ],
    },
    classifiers=[
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering",
        "Operating System :: Unix",
    ],
)
