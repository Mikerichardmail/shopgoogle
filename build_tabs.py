import os

layout_dir = r"f:\online shoping apps new\app\src\main\res\layout"

# 1. Categories Tab
categories_xml = """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#FAFAFA"
    android:orientation="vertical"
    android:padding="16dp">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Categories"
        android:textSize="24sp"
        android:textStyle="bold"
        android:textColor="#333333"
        android:layout_marginBottom="16dp"/>

    <!-- Gender Tabs -->
    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:gravity="center"
        android:layout_marginBottom="24dp">
        <TextView
            android:id="@+id/tabWomenCat"
            android:layout_width="0dp"
            android:layout_weight="1"
            android:layout_height="40dp"
            android:background="@drawable/bg_search"
            android:backgroundTint="#FFE4EC"
            android:gravity="center"
            android:text="Women"
            android:textColor="#E91E63"
            android:textStyle="bold" />
        <TextView
            android:id="@+id/tabMenCat"
            android:layout_width="0dp"
            android:layout_weight="1"
            android:layout_height="40dp"
            android:layout_marginStart="8dp"
            android:layout_marginEnd="8dp"
            android:background="@drawable/bg_search"
            android:backgroundTint="#E3F2FD"
            android:gravity="center"
            android:text="Men"
            android:textColor="#1976D2"
            android:textStyle="bold" />
        <TextView
            android:id="@+id/tabKidsCat"
            android:layout_width="0dp"
            android:layout_weight="1"
            android:layout_height="40dp"
            android:background="@drawable/bg_search"
            android:backgroundTint="#F3E5F5"
            android:gravity="center"
            android:text="Kids"
            android:textColor="#8E24AA"
            android:textStyle="bold" />
    </LinearLayout>

    <ScrollView
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:scrollbars="none">
        
        <GridLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:columnCount="2"
            android:rowCount="3"
            android:alignmentMode="alignMargins"
            android:columnOrderPreserved="false">

            <!-- Electronics -->
            <androidx.cardview.widget.CardView
                android:layout_width="0dp"
                android:layout_height="120dp"
                android:layout_columnWeight="1"
                android:layout_margin="8dp"
                app:cardCornerRadius="16dp"
                app:cardElevation="2dp">
                <LinearLayout
                    android:layout_width="match_parent"
                    android:layout_height="match_parent"
                    android:background="@drawable/cat_electronics_gradient"
                    android:gravity="center"
                    android:orientation="vertical">
                    <ImageView android:layout_width="40dp" android:layout_height="40dp" android:src="@drawable/ic_laptop" app:tint="#FFFFFF"/>
                    <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Electronics" android:textColor="#FFFFFF" android:textStyle="bold" android:layout_marginTop="8dp"/>
                </LinearLayout>
            </androidx.cardview.widget.CardView>

            <!-- Fashion -->
            <androidx.cardview.widget.CardView
                android:layout_width="0dp"
                android:layout_height="120dp"
                android:layout_columnWeight="1"
                android:layout_margin="8dp"
                app:cardCornerRadius="16dp"
                app:cardElevation="2dp">
                <LinearLayout
                    android:layout_width="match_parent"
                    android:layout_height="match_parent"
                    android:background="@drawable/cat_fashion_gradient"
                    android:gravity="center"
                    android:orientation="vertical">
                    <ImageView android:layout_width="40dp" android:layout_height="40dp" android:src="@drawable/ic_bag" app:tint="#FFFFFF"/>
                    <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Fashion" android:textColor="#FFFFFF" android:textStyle="bold" android:layout_marginTop="8dp"/>
                </LinearLayout>
            </androidx.cardview.widget.CardView>

            <!-- Beauty -->
            <androidx.cardview.widget.CardView
                android:layout_width="0dp"
                android:layout_height="120dp"
                android:layout_columnWeight="1"
                android:layout_margin="8dp"
                app:cardCornerRadius="16dp"
                app:cardElevation="2dp">
                <LinearLayout
                    android:layout_width="match_parent"
                    android:layout_height="match_parent"
                    android:background="@drawable/cat_beauty_gradient"
                    android:gravity="center"
                    android:orientation="vertical">
                    <ImageView android:layout_width="40dp" android:layout_height="40dp" android:src="@drawable/ic_heart" app:tint="#FFFFFF"/>
                    <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Beauty" android:textColor="#FFFFFF" android:textStyle="bold" android:layout_marginTop="8dp"/>
                </LinearLayout>
            </androidx.cardview.widget.CardView>

            <!-- Health -->
            <androidx.cardview.widget.CardView
                android:layout_width="0dp"
                android:layout_height="120dp"
                android:layout_columnWeight="1"
                android:layout_margin="8dp"
                app:cardCornerRadius="16dp"
                app:cardElevation="2dp">
                <LinearLayout
                    android:layout_width="match_parent"
                    android:layout_height="match_parent"
                    android:background="@drawable/cat_health_gradient"
                    android:gravity="center"
                    android:orientation="vertical">
                    <ImageView android:layout_width="40dp" android:layout_height="40dp" android:src="@drawable/ic_heart" app:tint="#FFFFFF"/>
                    <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Health" android:textColor="#FFFFFF" android:textStyle="bold" android:layout_marginTop="8dp"/>
                </LinearLayout>
            </androidx.cardview.widget.CardView>

        </GridLayout>
    </ScrollView>
</LinearLayout>
"""
with open(os.path.join(layout_dir, "fragment_categories.xml"), "w", encoding="utf-8") as f:
    f.write(categories_xml)

# 2. Coupons Tab
coupons_xml = """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#FAFAFA"
    android:orientation="vertical"
    android:padding="16dp">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="All Coupons"
        android:textSize="24sp"
        android:textStyle="bold"
        android:textColor="#333333"
        android:layout_marginBottom="16dp"/>

    <EditText
        android:id="@+id/etSearchCoupons"
        android:layout_width="match_parent"
        android:layout_height="48dp"
        android:background="@drawable/bg_search"
        android:drawableStart="@drawable/ic_search"
        android:drawablePadding="12dp"
        android:hint="Search codes or stores..."
        android:paddingStart="16dp"
        android:paddingEnd="16dp"
        android:textSize="14sp"
        android:layout_marginBottom="16dp"/>

    <!-- Filters -->
    <HorizontalScrollView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:scrollbars="none"
        android:layout_marginBottom="16dp">
        <LinearLayout
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:orientation="horizontal">
            <TextView android:layout_width="wrap_content" android:layout_height="32dp" android:background="@drawable/bg_search" android:backgroundTint="#333" android:textColor="#fff" android:text="All" android:gravity="center" android:paddingStart="16dp" android:paddingEnd="16dp" android:layout_marginEnd="8dp"/>
            <TextView android:layout_width="wrap_content" android:layout_height="32dp" android:background="@drawable/bg_search" android:backgroundTint="#E5E7EB" android:textColor="#333" android:text="Verified Today" android:gravity="center" android:paddingStart="16dp" android:paddingEnd="16dp" android:layout_marginEnd="8dp"/>
            <TextView android:layout_width="wrap_content" android:layout_height="32dp" android:background="@drawable/bg_search" android:backgroundTint="#E5E7EB" android:textColor="#333" android:text="High Success Rate" android:gravity="center" android:paddingStart="16dp" android:paddingEnd="16dp" />
        </LinearLayout>
    </HorizontalScrollView>

    <androidx.recyclerview.widget.RecyclerView
        android:id="@+id/rvAllCoupons"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:clipToPadding="false"
        android:paddingBottom="80dp"/>
</LinearLayout>
"""
with open(os.path.join(layout_dir, "fragment_coupons.xml"), "w", encoding="utf-8") as f:
    f.write(coupons_xml)

# 3. Stores Tab
stores_xml = """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#FAFAFA"
    android:orientation="vertical"
    android:padding="16dp">

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:gravity="center_vertical"
        android:layout_marginBottom="16dp">
        <TextView
            android:layout_width="0dp"
            android:layout_weight="1"
            android:layout_height="wrap_content"
            android:text="Store Directory"
            android:textSize="24sp"
            android:textStyle="bold"
            android:textColor="#333333"/>
        <TextView
            android:id="@+id/btnFavToggle"
            android:layout_width="wrap_content"
            android:layout_height="36dp"
            android:background="@drawable/bg_search"
            android:backgroundTint="#FFE4EC"
            android:gravity="center"
            android:paddingStart="16dp"
            android:paddingEnd="16dp"
            android:text="❤️ Fav"
            android:textColor="#E91E63"
            android:textStyle="bold" />
    </LinearLayout>

    <EditText
        android:id="@+id/etSearchStores"
        android:layout_width="match_parent"
        android:layout_height="48dp"
        android:background="@drawable/bg_search"
        android:drawableStart="@drawable/ic_search"
        android:drawablePadding="12dp"
        android:hint="Search any store..."
        android:paddingStart="16dp"
        android:paddingEnd="16dp"
        android:textSize="14sp"
        android:layout_marginBottom="16dp"/>

    <androidx.recyclerview.widget.RecyclerView
        android:id="@+id/rvAllStores"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:clipToPadding="false"
        android:paddingBottom="80dp"/>
</LinearLayout>
"""
with open(os.path.join(layout_dir, "fragment_stores.xml"), "w", encoding="utf-8") as f:
    f.write(stores_xml)

# 4. Profile Tab
profile_xml = """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#FAFAFA"
    android:orientation="vertical">

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:background="@drawable/cat_beauty_gradient"
        android:padding="32dp"
        android:gravity="center"
        android:orientation="vertical">
        <ImageView
            android:layout_width="80dp"
            android:layout_height="80dp"
            android:src="@drawable/ic_home"
            app:tint="#FFFFFF"
            android:background="@drawable/bg_search"
            android:backgroundTint="#33FFFFFF"
            android:padding="16dp"/>
        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Hello, Shopper!"
            android:textColor="#FFFFFF"
            android:textSize="22sp"
            android:textStyle="bold"
            android:layout_marginTop="16dp"/>
        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Sign in to sync your saved coupons"
            android:textColor="#EEFFFFFF"
            android:textSize="14sp"
            android:layout_marginTop="4dp"/>
    </LinearLayout>

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="vertical"
        android:padding="24dp">

        <TextView android:id="@+id/btnShareApp" android:layout_width="match_parent" android:layout_height="56dp" android:text="↗️  Share App" android:gravity="center_vertical" android:textSize="16sp" android:textColor="#333" android:background="?attr/selectableItemBackground"/>
        <View android:layout_width="match_parent" android:layout_height="1dp" android:background="#E5E7EB"/>
        
        <TextView android:layout_width="match_parent" android:layout_height="56dp" android:text="❤️  Saved Coupons" android:gravity="center_vertical" android:textSize="16sp" android:textColor="#333" android:background="?attr/selectableItemBackground"/>
        <View android:layout_width="match_parent" android:layout_height="1dp" android:background="#E5E7EB"/>
        
        <TextView android:layout_width="match_parent" android:layout_height="56dp" android:text="⚙️  Settings" android:gravity="center_vertical" android:textSize="16sp" android:textColor="#333" android:background="?attr/selectableItemBackground"/>
        <View android:layout_width="match_parent" android:layout_height="1dp" android:background="#E5E7EB"/>
        
        <TextView android:layout_width="match_parent" android:layout_height="56dp" android:text="📄  Privacy Policy" android:gravity="center_vertical" android:textSize="16sp" android:textColor="#333" android:background="?attr/selectableItemBackground"/>

    </LinearLayout>

</LinearLayout>
"""
with open(os.path.join(layout_dir, "fragment_profile.xml"), "w", encoding="utf-8") as f:
    f.write(profile_xml)

print("Created all 4 layout xmls.")
