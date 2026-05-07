import os
import re

app_dir = r"f:\online shoping apps new\app\src\main"
java_dir = os.path.join(app_dir, "java", "com", "onlineshoppingapps")
res_dir = os.path.join(app_dir, "res")
layout_dir = os.path.join(res_dir, "layout")

# 1. READ activity_main.xml
activity_main_path = os.path.join(layout_dir, "activity_main.xml")
with open(activity_main_path, "r", encoding="utf-8") as f:
    activity_xml = f.read()

# Extract the NestedScrollView block
scroll_start = activity_xml.find("<androidx.core.widget.NestedScrollView")
scroll_end = activity_xml.rfind("</androidx.core.widget.NestedScrollView>") + len("</androidx.core.widget.NestedScrollView>")

nested_scroll = activity_xml[scroll_start:scroll_end]

# Create fragment_home.xml
fragment_home_xml = f"""<?xml version="1.0" encoding="utf-8"?>
{nested_scroll}
"""
# Remove layout_above from NestedScrollView in fragment_home.xml
fragment_home_xml = re.sub(r'android:layout_above="[^"]+"', '', fragment_home_xml)

with open(os.path.join(layout_dir, "fragment_home.xml"), "w", encoding="utf-8") as f:
    f.write(fragment_home_xml)

# Update activity_main.xml
fragment_container = """
    <androidx.fragment.app.FragmentContainerView
        android:id="@+id/fragmentContainer"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:layout_above="@id/bottomNavigation" />
"""
new_activity_xml = activity_xml[:scroll_start] + fragment_container + activity_xml[scroll_end:]
with open(activity_main_path, "w", encoding="utf-8") as f:
    f.write(new_activity_xml)

# Create placeholder layouts for other fragments
placeholders = ["categories", "coupons", "stores", "profile"]
for ph in placeholders:
    ph_xml = f"""<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:gravity="center"
    android:background="#FAFAFA"
    android:orientation="vertical">
    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="{ph.capitalize()} Tab"
        android:textSize="24sp"
        android:textStyle="bold"
        android:textColor="#333333"/>
</LinearLayout>
"""
    with open(os.path.join(layout_dir, f"fragment_{ph}.xml"), "w", encoding="utf-8") as f:
        f.write(ph_xml)

print("Layouts refactored.")
