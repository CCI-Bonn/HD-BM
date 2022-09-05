# HD-BM

## Introduction

This repository provides easy to use access to our HD-BM brain metastasis segmentation tool.
HD-BM is the result of a joint project between the Department of Neuroradiology at the Heidelberg University Hospital,
Germany and the Division of Medical Image Computing at the German Cancer Research Center (DKFZ) Heidelberg, Germany.
If you are using HD-BM, please cite the following publications:

1. Pflüger, I., Wald, T., Isensee, F., et al. (2022). Automated detection and quantification of brain metastases on clinical MRI data using artificial neural networks.
   Neuro-Oncology Advances. vdac138. https://doi.org/10.1093/noajnl/vdac138
   
2. Isensee, F., Jaeger, P. F., Kohl, S. A., Petersen, J., & Maier-Hein, K. H. (2020). nnU-Net: a self-configuring method 
for deep learning-based biomedical image segmentation. Nature Methods, 1-9.


HD-BM was developed with 308 patients with clinically diagnosed BM from several primary tumors that were
treated at the Heidelberg University Hospital (Heidelberg, Germany) and who underwent standardized
MRI examination at the Department of Neuroradiology for radiation therapy between 2011 and 2018.
The patients were assigned to either training or test set with a 4:1 ratio.
Specifically, the training set consisted of n = 246 patients 
(with n = 246 MRI exams, i.e., one exam per patient) at any point in the disease course,
whereas the institutional test set consisted of n = 62 patients. HD-BM was further validated
on an external test set of 30 adult patients with BMs from the Heidelberg Thoracic Clinic, 
mainly originating from lung cancer, treated between 2013 and 2019.  

MRI exams were acquired with a 3-T MR imaging system (Magnetom Verio, Skyra or Trio TIM; Siemens Healthcare)
except a single measurement which was acquired on a 1.5-T field strength (Magnetom Avanto;
Siemens Healthineers). All MRI exams of the external test set were acquired on a 1.5-T 
MRI system (Magnetom Avanto; Siemens Healthineers).
All MRI scans in all Datasets included T1-weighted images before and
after gadolinium contrast agent and FLAIR images (detailed description of acquisition
parameters in the Supplement).

Given these modalities we provide two models that are capable to automatically predict BM of patients:
1. `HD-BM`, which uses a T1-weighted, contrast enhanced T1-weighted, FLAIR and a T1-subtraction image
2. `HD-BM Slim`, which only needs a contrast enhanced T1-weighted and a FLAIR image


## Installation Instructions

### Installation Requirements
HD-BM only runs on Linux with python3.
Supported python3 versions are python3.6. Python 3.9 doesn't work as downloading of weights breaks. (Might work after downloading the [weights](https://zenodo.org/record/4915908) manually and extracting them in the directory specified by `paths.py`).
In order to run a pc with a GPU with at least 4 GB of VRAM and cuda/pytorch support is required. Running the prediction on CPU is not supported.

### Installation with Pip
Installation with pip is currently not supported.

### Manual installation
We generally recommend to create a new virtualenv for every project that is installed so package dependencies don't get mixed.
To test if virtualenv is installed call `virtualenv --version`. This will return something like this: `virtualenv 20.0.17 from <SOME_PATH>` should it be installed.
([Should it not be installed follow this how-to to install it (Optional).](https://linoxide.com/linux-how-to/setup-python-virtual-environment-ubuntu/))

#### Installing with a virtualenv
```shell
# With virtualenv
virtualenv HD-BM-env --python=python3.6  # Creates a new Virtual environment 
source HD-BM-env/bin/activate  # Activates the environment

git clone git@github.com:NeuroAI-HD/HD-BM.git  # Clones the Repository
pip install HD-BM/  # Install the repository for the current virtualenv
```
#### Installing without virtualenv
```shell
# Without virtualenv
git clone git@github.com:NeuroAI-HD/HD-BM.git  # Clones the repository
pip3 install HD-BM/  # Installs the repository for the python3 interpreter
```

This will install `HD-BM` commands directly onto your system (or the virtualenv). You can use them from anywhere (when the virtualenv is active).

## How to use it
Using HD-BM is straight forward. After installing you can call `hd_bm_predict` or `hd_bm_predict_folder` to predict cases with all four MRI modalities or
call `hd_bm_slim_predict` or `hd_bm_slim_folder` to predict cases that are imaged with contrast enhanced T1-weighted and FLAIR MRI sequence.

As these commands are called for the first time the weights for the nnUNet model will be downloaded automatically and saved to your home directory.
Should you want to change the location where weights are to be stored edit the file located in `/<YOUR_PATH>/HD-BM/hd_bm/paths.py`.

## Prerequisites
HD-BM was trained with two/four MRI modalities: (optional) T1,constrast-enhanced T1, FLAIR and (optional), T1 subtraction image.

All input files must be provided as nifti (.nii.gz) files containing 2D or 3D MRI image data.
Sequences with multiple temporal volumes (i.e. 4D sequences) are not supported (however can be split upfront into the individual temporal volumes using fslsplit1).
- T1 inputs must be a T1-weighted sequence before contrast-agent administration (T1-w) acquired as 2D with axial orientation (e.g. TSE) or as 3D (e.g. MPRAGE)
- cT1 inputs must be a T1-weighted sequence after contrast-agent administration (cT1-w) acquired as 2D with axial orientation (e.g. TSE) or as 3D (e.g. MPRAGE)
- FLAIR inputs must be a fluid attenuated inversion recovery (FLAIR) sequence acquired as 2D with axial orientation (e.g. TSE). A 3D acquisition (e.g. 3D TSE/FSE) may work as well.
- T1sub must be a substraction image between cT1 and T1 `T1sub = (cT1 - T1)` inputs after coregistration

(These specifications are in line with the consensus recommendations for a standardized brain tumor imaging protocol in clinical trials - see Ellingson et al. Neuro Oncol. 2015 Sep;17(9):1188-98 - www.ncbi.nlm.nih.gov/pubmed/26250565)

Input files must contain 3D images; Sequences with multiple temporal volumes (i.e. 4D sequences) are not supported (however can be split upfront into the individual temporal volumes using fslsplit1).

All input files must match the orientation of standard MNI152 template and must be brain extracted and co-registered. All non-brain voxels must be 0. To ensure that these pre-processing steps are performed correctly you may adhere to the following example:

#### Reorient MRI sequences to standard space
```shell
fslreorient2std T1.nii.gz T1_reorient.nii.gz
fslreorient2std CT1.nii.gz CT1_reorient.nii.gz
fslreorient2std FLAIR.nii.gz FLAIR_reorient.nii.gz
```

#### The following is the recommended workflow for FSL5. There is a better way to do this but this requires FSL6 (see below)

```shell
# perform brain extraction using HD-BET (https://github.com/MIC-DKFZ/HD-BET)
hd-bet -i T1_reorient.nii.gz
hd-bet -i CT1_reorient.nii.gz
hd-bet -i FLAIR_reorient.nii.gz

# register all sequences to T1
fsl5.0-flirt -in CT1_reorient_bet.nii.gz -ref T1_reorient_bet.nii.gz -out CT1_reorient_bet_reg.nii.gz -dof 6 -interp spline
fsl5.0-flirt -in T2_reorient_bet.nii.gz -ref T1_reorient.nii.gz -out T2_reorient_bet_reg.nii.gz -dof 6 -interp spline
fsl5.0-flirt -in FLAIR_reorient_bet.nii.gz -ref T1_reorient.nii.gz -out FLAIR_reorient_bet_reg.nii.gz -dof 6 -interp spline

# Create T1sub by subtracting CT1 - T1

# reapply T1 brain mask (this is important because HD-BM expects non-brain voxels to be 0 and the registration process can introduce nonzero values
# T1_BRAIN_MASK.nii.gz is the mask (not the brain extracted image!) as obtained from HD-Bet
fsl5.0-fslmaths CT1_reorient_bet_reg.nii.gz -mas T1_BRAIN_MASK.nii.gz CT1_reorient_bet_reg.nii.gz
fsl5.0-fslmaths T2_reorient_bet_reg.nii.gz -mas T1_BRAIN_MASK.nii.gz T2_reorient_bet_reg.nii.gz
fsl5.0-fslmaths FLAIR_reorient_bet_reg.nii.gz -mas T1_BRAIN_MASK.nii.gz FLAIR_reorient_bet_reg.nii.gz
fsl5.0-fslmaths T1sub_reorient_bet_reg.nii.gz -mas T1_BRAIN_MASK.nii.gz T1sub_reorient_bet_reg.nii.gz
```

#### This is how to do it with FSL6:
```shell
# run hd bet
hd-bet -i T1_reorient.nii.gz -o t1_bet.nii.gz -s 1
hd-bet -i CT1_reorient.nii.gz -o ct1_bet.nii.gz
hd-bet -i FLAIR_reorient.nii.gz -o flair_bet.nii.gz

# register brain extracted images to t1, save matrix
flirt -in ct1_bet.nii.gz -out ct1_bet_reg.nii.gz -ref t1_bet.nii.gz -omat ct1_to_t1.mat -interp spline -dof 6 &
flirt -in flair_bet.nii.gz -out flair_bet_reg.nii.gz -ref t1_bet.nii.gz -omat flair_to_t1.mat -interp spline -dof 6 &
wait

# Create the T1Sub by subtracting CT1 - T1

# we are only interested in the matrices, delete the other output images
rm ct1_bet.nii.gz flair_bet.nii.gz
rm ct1_bet_reg.nii.gz flair_bet_reg.nii.gz

# now apply the transformation matrices to the original images (pre hd-bet)
flirt -in CT1_reorient.nii.gz -out ct1_reg.nii.gz -ref t1_bet.nii.gz -applyxfm -init ct1_to_t1.mat -interp spline &
flirt -in FLAIR_reorient.nii.gz -out flair_reg.nii.gz -ref t1_bet.nii.gz -applyxfm -init flair_to_t1.mat -interp spline &
wait

# now apply t1 brain mask to all registered images
fslmaths ct1_reg.nii.gz -mas t1_bet_mask.nii.gz CT1_reorient_reg_bet.nii.gz & # t1_bet_mask.nii.gz was generated by hd-bet (see above)
fslmaths flair_reg.nii.gz -mas t1_bet_mask.nii.gz FLAIR_reorient_reg_bet.nii.gz & # t1_bet_mask.nii.gz was generated by hd-bet (see above)
fslmaths T1sub_reg.nii.gz -mas t1_bet_mask.nii.gz T1sub_reorient_reg_bet.nii.gz & # t1_bet_mask.nii.gz was generated by hd-bet (see above)
wait

# done
```
After applying this example you would use `T1_reorient.nii.gz`, `CT1_reorient_reg_bet.nii.gz`, `FLAIR_reorient_reg_bet.nii.gz` and `T1sub_reori to proceed.

## Run HD-BM
HD-BM provides four main scripts: `hd_bm_predict` and `hd_bm_predict_folder` for with T1, T1ce, FLAIR and T1sub modalities are provided.

For cases that do not have T1 and T1sub modalities `hd_bm_slim_predict` and `hd_bm_slim_predict_folder` can be used instead.

### Predicting cases
The models take multiple modalities as input, which have to be formatted in a nnUNet style fashion (i.e. `{ARBITRARY_IMAGE_ID}_{MODALITY_ID}.nii.gz`).
See [original nnUNet docu](https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/dataset_conversion.md) for more information about that.

For cases that are imaged with T1, cT1, FLAIR and T1sub the `MODALITY_ID` has to be: `{T1: 0000, cT1: 0001, FLAIR: 0002, T1sub: 0003}`, for the corresponding modality.
For cases imaged __without__ T1 and T1sub the `MODALITY_ID` has to be: `{T1ce: 0000, FLAIR: 0001}`, for the corresponding modalities.
The user has to confirm this when running or skip the check by using the `--skip_modality_check 1` option. 

### Predicting a single case
`hd_bm_predict` and `hd_bm_slim_predict` can be used to predict a single case. 
This can be useful for exploration or if the number of cases to be processed is low. Exemplary use of it:

`hd_bm_predict -i INPUT_DIR -id ARBITRARY_IMAGE_ID -o OUTPUT_DIR -oid OUTPUT_ID`

`INPUT_DIR` is the path to the directory that contains the images of the patient.
`ARBITRARY_IMAGE_ID` can be either only the identifier or any image with/without the `MODALITY_ID`.
`OUTPUT_DIR` is the path to the output directory to save the image to, if it does not exist all directories that are missing will be created.
`OUTPUT_ID` is an _optional_ name for the output, if not given the input image ID will be used instead.

For further information use the help option that comes with each command, providing a detailed explanation. (e.g. `hd_bm_predict --help`).

### Predicting multiple cases
`hd_bm_predict_folder` / `hd_bm_predict_slim_predict_folder` is useful for batch processing, especially if the number of cases to be processed is large.
By interleaving preprocessing, inference and segmentation export we can speed up the prediction significantly. Furthermore, the pipeline is initialized only once for all cases,
again saving a lot of computation and I/O time.  Here is how to use it:

`hd_bm_predict_folder -i INPUT_DIR -o OUTPUT_DIR`

The `INPUT_DIR` must contain nifti images (.nii.gz). The results will be written to the `OUTPUT_DIR` (with the same file names).
 If the output folder does not exist it will be created.
