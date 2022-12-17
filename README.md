# KODxAuto
WIP Automation framework (package) for automating manual tasks utilizing image recognition for element selection on the screen.

# Usage
### Import
```py
import kodxauto
```
### Call
```py
kxa = kodxauto.KODxAuto()
kxa.set_root_dir("./")      # Root directory of your project
kxa.run()                   # Set macros name in properties file or pass as a string
```
### Properties
Create a file `kodxauto.properties` in the root directory of your project.

```properties
[settings]
# All paths are set relative to this config file
macros_folder_path = ./macros
log_file_path = ./kodxauto.log
custom_step_definitions_paths = []
macro_name = happy
recompile = 1
```