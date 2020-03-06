from decouple import config


experiment_name = """An experiment is all the images performed on a single set of samples. All images associated with a single set of samples should be uploaded under the same experiment.  The experiment name allows it to be looked up later under the search experiments tab. Images can be uploaded to an existing experiment."""
experiment_project = """The project encompasses a related set of images and experiments, such as all the images associated with a paper. If you do not see your project, you can simply add one by clicking create."""
experiment_lab = """The PI of the lab to which this image belongs. More than one lab can be selected. If you do not see your PI’s name please email {} at {} to request it be added. You must wait until your PI has been added before you can upload the image.""".format(config('SUPPORT_NAME'), config('SUPPORT_EMAIL'))
experiment_organism = """The organism(s) that this sample consists of. More than one organism can be selected. If you do not see the organism you need, please email {} at {} to request it be added. You must wait until the organism(s) have been added before you can upload your image.""".format(config('SUPPORT_NAME'), config('SUPPORT_EMAIL'))
experiment_vessel = """The vessel in which the organism was grown.  If you do not see the option you need, you may select other."""
experiment_substratum = """The substratum the organism was grown on. If you do not see the option you need, you may select other. """

image_document = """Info"""
image_date_taken = """Info"""
image_release_date = """The date after which this image will be viewable by all users; before this date, the image is hidden. This keeps ongoing research information private. """
image_imager = """The person who took the image. If you do not see the imager’s name, you may add it by clicking create."""
image_microscope_setting = """The microscope used, the objective, and the medium the image was taken through."""
image_breif_description = ''' A quick summary of the image, such as “a medical biofilm treated with daptomycin”.'''
image_raw_data_location = """The location of the raw image file from the microscope, such as your personal computer or a CBE server."""
