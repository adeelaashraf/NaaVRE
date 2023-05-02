import os

class Rcontainerizer:

    @staticmethod
    def get_files_info(cell=None, image_repo=None, cells_path=None):
        if not os.path.exists(cells_path):
            os.mkdir(cells_path)
        cell_path = os.path.join(cells_path, cell.task_name)

        cell_file_name = cell.task_name + '.R'
        dockerfile_name = 'Dockerfile.' + image_repo + '.' + cell.task_name
        environment_file_name = cell.task_name + '-environment.yaml'

        if os.path.exists(cell_path):
            for files in os.listdir(cell_path):
                path = os.path.join(cell_path, files)
                if os.path.isfile(path):
                    os.remove(path)
        else:
            os.mkdir(cell_path)

        cell_file_path = os.path.join(cell_path, cell_file_name)
        dockerfile_file_path = os.path.join(cell_path, dockerfile_name)
        env_file_path = os.path.join(cell_path, environment_file_name)
        return {'cell': {
            'file_name': cell_file_name,
            'path': cell_file_path},
            'dockerfile': {
                'file_name': dockerfile_name,
                'path': dockerfile_file_path},
            'environment': {
                'file_name': environment_file_name,
                'path': env_file_path}
        }
    
    @staticmethod 
    def build_templates(cell=None, files_info=None):
  
        # create the source code file
        with open(files_info['cell']['path'], "w") as file:
            file.write("setwd('/app') \n")

            # in case there are input types, we should dynamically add this value to the script
            # this is done using the 'optparse' library, which does something similar as in the Python script
            if len(cell.types) > 0:
                file.write("library(optparse) \n")
                file.write("option_list = list( \n")

                for i, (key, value) in enumerate(cell.types.items()): # TODO: support more types and write more clean
                    type = None
                    if value == "str":
                        type = "character"
                    elif value == "int":
                        type = "integer"
                    else:
                        raise ValueError("Not a valid type")

                    file.write('''\t make_option(c("--{}"), action="store", default=NA, type='{}', help="my description")'''.format(key, type)) # https://gist.github.com/ericminikel/8428297
                    
                    if i != len(cell.types) - 1:
                        file.write(",")
                    file.write("\n")

                file.write(")\n\n")
                file.write("opt = parse_args(OptionParser(option_list=option_list)) \n\n")

            # replace inputs
            original_source = cell.original_source
            for key, value in cell.types.items():
                original_source = original_source.replace(key, "opt$" + key)
            file.write(original_source)

        # create the Dockerfile
        with open(files_info['dockerfile']['path'], "w") as file:
            
            # Step 1: base image.
            file.write("FROM {}\n\n".format(cell.base_image))
            file.write("USER root \n\n") # in case of this image, we need root permissions

            # Step 2: install dependencies. for now, a naive way
            print(cell.dependencies)
            for dep in cell.dependencies:
                file.write('''RUN R -e "install.packages('{}', repos='http://cran.rstudio.com')" \n'''.format(dep['name']))
            file.write("\n")

            file.write("RUN mkdir -p /app \n")
            file.write("COPY {} /app".format(files_info['cell']['file_name']))

