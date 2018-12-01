timetracker="~/Projects/TimeTracker/"
folder=$folder"archive/$(date +%G)/$(date +%B)/$(date +%d)/"
mkdir -p "$folder"

cat "log" >> "$folder/log"
rm "log"

function save_input(){
  read -p "$1 ($(cat "$folder""$2")): " input
  input=${input:-$(cat "$folder""$2")}
  echo $input > $folder"$2"
}

save_input "Audible minutes" audible
save_input "Wake Time" waking
save_input "Sleep Time" sleeping
save_input "Meditating Time" meditating
save_input "Running Time" running
save_input "Music minutes" music
save_input "Brushing Teeth" brushing_teeth
save_input "Shower Time" shower
save_input "Shaving Time" shaving
save_input "Dishes time" dishes
save_input "Reading time" reading
save_input "Weightlifting time" weightlifting
save_input "Plank time" plank
save_input "Breakfast time" breakfast
save_input "Lunch time" lunch
save_input "Dinner time" dinner
save_input "Tutoring time" tutoring
save_input "Driving time" driving
save_input "Meeting time" meeting
