application=$(i3-msg -t get_tree | python ~/Projects/TimeTracker/extract_focused.py)

if [ "$application" = "URxvt" ]; then
  echo "$(date +%s) $(i3-msg -t get_tree | python ~/Projects/TimeTracker/extract_focused.py) $(cat ~/Projects/TimeTracker/pwd)" >> ~/Projects/TimeTracker/log
elif [ "$application" = "Firefox" ]; then
  echo "$(date +%s) $(i3-msg -t get_tree | python ~/Projects/TimeTracker/extract_focused.py) $(python ~/Projects/TimeTracker/get_history.py)" >> ~/Projects/TimeTracker/log
else
  echo "$(date +%s) $(i3-msg -t get_tree | python ~/Projects/TimeTracker/extract_focused.py)" >> ~/Projects/TimeTracker/log
fi
