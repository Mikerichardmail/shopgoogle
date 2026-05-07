import os

res_dir = r"f:\online shoping apps new\app\src\main\res"

def write_file(path, content):
    full_path = os.path.join(res_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"Created {path}")

# 1. Colors
write_file(r"color\bottom_nav_color.xml", """
<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:color="#E91E63" android:state_checked="true" />
    <item android:color="#999999" />
</selector>
""")

# 2. Drawables
write_file(r"drawable\ic_menu.xml", """
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24">
    <path android:fillColor="#000000" android:pathData="M3,18h18v-2H3v2zm0,-5h18v-2H3v2zm0,-7v2h18V6H3z"/>
</vector>
""")

write_file(r"drawable\ic_bell.xml", """
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24">
    <path android:fillColor="#000000" android:pathData="M12,22c1.1,0 2,-0.9 2,-2h-4c0,1.1 0.9,2 2,2zm6,-6v-5c0,-3.07 -1.63,-5.64 -4.5,-6.32V4c0,-0.83 -0.67,-1.5 -1.5,-1.5s-1.5,0.67 -1.5,1.5v0.68C7.64,5.36 6,7.92 6,11v5l-2,2v1h16v-1l-2,-2zm-2,1H8v-6c0,-2.48 1.51,-4.5 4,-4.5s4,2.02 4,4.5v6z"/>
</vector>
""")

write_file(r"drawable\ic_home.xml", """
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24">
    <path android:fillColor="#000000" android:pathData="M10,20v-6h4v6h5v-8h3L12,3 2,12h3v8z"/>
</vector>
""")

write_file(r"drawable\ic_category.xml", """
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24">
    <path android:fillColor="#000000" android:pathData="M3,13h8V3H3v10zm0,8h8v-6H3v6zm10,0h8V11h-8v10zm0,-18v6h8V3h-8z"/>
</vector>
""")

write_file(r"drawable\ic_coupon_nav.xml", """
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24">
    <path android:fillColor="#000000" android:pathData="M21.41,11.58l-9,-9C12.05,2.22 11.55,2 11,2H4C2.9,2 2,2.9 2,4v7c0,0.55 0.22,1.05 0.59,1.42l9,9c0.36,0.36 0.86,0.58 1.41,0.58 0.55,0 1.05,-0.22 1.41,-0.59l7,-7c0.37,-0.36 0.59,-0.86 0.59,-1.41 0,-0.55 -0.23,-1.06 -0.59,-1.42zM5.5,7C4.67,7 4,6.33 4,5.5S4.67,4 5.5,4 7,4.67 7,5.5 6.33,7 5.5,7z"/>
</vector>
""")

write_file(r"drawable\ic_store_nav.xml", """
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24">
    <path android:fillColor="#000000" android:pathData="M20,4H4v2h16V4zm1,10v-2l-1,-5H4l-1,5v2h1v6h10v-6h4v6h2v-6h1zm-9,4H6v-4h6v4z"/>
</vector>
""")

write_file(r"drawable\ic_profile.xml", """
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24">
    <path android:fillColor="#000000" android:pathData="M12,12c2.21,0 4,-1.79 4,-4s-1.79,-4 -4,-4 -4,1.79 -4,4 1.79,4 4,4zm0,2c-2.67,0 -8,1.34 -8,4v2h16v-2c0,-2.66 -5.33,-4 -8,-4z"/>
</vector>
""")

write_file(r"drawable\bg_badge.xml", """
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="oval">
    <solid android:color="#E91E63" />
    <stroke android:width="1dp" android:color="#FFFFFF" />
</shape>
""")

# 3. Menu
write_file(r"menu\bottom_nav_menu.xml", """
<?xml version="1.0" encoding="utf-8"?>
<menu xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:id="@+id/nav_home" android:icon="@drawable/ic_home" android:title="Home" />
    <item android:id="@+id/nav_categories" android:icon="@drawable/ic_category" android:title="Categories" />
    <item android:id="@+id/nav_coupons" android:icon="@drawable/ic_coupon_nav" android:title="Coupons" />
    <item android:id="@+id/nav_stores" android:icon="@drawable/ic_store_nav" android:title="Stores" />
    <item android:id="@+id/nav_profile" android:icon="@drawable/ic_profile" android:title="Profile" />
</menu>
""")

# 4. Activity Main Update
write_file(r"layout\activity_main.xml", """
<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#FAFAFA">

    <!-- ===== BOTTOM NAVIGATION ===== -->
    <com.google.android.material.bottomnavigation.BottomNavigationView
        android:id="@+id/bottomNavigation"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_alignParentBottom="true"
        android:background="#FFFFFF"
        app:itemIconTint="@color/bottom_nav_color"
        app:itemTextColor="@color/bottom_nav_color"
        app:menu="@menu/bottom_nav_menu"
        android:elevation="8dp"/>

    <!-- ===== SCROLLABLE CONTENT ===== -->
    <androidx.core.widget.NestedScrollView
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:layout_above="@id/bottomNavigation"
        android:scrollbars="none"
        android:fillViewport="true">

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="vertical"
            android:paddingBottom="24dp">

            <!-- ===== TOP BAR ===== -->
            <LinearLayout
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:orientation="horizontal"
                android:gravity="center_vertical"
                android:paddingStart="16dp"
                android:paddingEnd="16dp"
                android:paddingTop="16dp"
                android:paddingBottom="12dp">

                <ImageView
                    android:id="@+id/ivMenu"
                    android:layout_width="28dp"
                    android:layout_height="28dp"
                    android:src="@drawable/ic_menu"
                    app:tint="#333333" />

                <LinearLayout
                    android:layout_width="0dp"
                    android:layout_height="wrap_content"
                    android:layout_weight="1"
                    android:layout_marginStart="12dp"
                    android:gravity="center_vertical"
                    android:orientation="horizontal">
                    
                    <ImageView
                        android:layout_width="24dp"
                        android:layout_height="24dp"
                        android:src="@drawable/ic_heart"
                        app:tint="#E91E63" />
                        
                    <TextView
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:text="Shop"
                        android:textColor="#333333"
                        android:textSize="20sp"
                        android:textStyle="bold"
                        android:layout_marginStart="4dp"/>
                    <TextView
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:text="Saver"
                        android:textColor="#E91E63"
                        android:textSize="20sp"
                        android:textStyle="bold" />
                </LinearLayout>

                <RelativeLayout
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:layout_marginEnd="16dp">
                    
                    <ImageView
                        android:id="@+id/ivNotification"
                        android:layout_width="26dp"
                        android:layout_height="26dp"
                        android:src="@drawable/ic_bell"
                        app:tint="#333333" />
                        
                    <TextView
                        android:layout_width="16dp"
                        android:layout_height="16dp"
                        android:background="@drawable/bg_badge"
                        android:text="3"
                        android:textColor="#FFFFFF"
                        android:textSize="10sp"
                        android:gravity="center"
                        android:layout_alignTop="@id/ivNotification"
                        android:layout_alignEnd="@id/ivNotification"
                        android:layout_marginTop="-4dp"
                        android:layout_marginEnd="-4dp"/>
                </RelativeLayout>

                <ImageView
                    android:id="@+id/ivTopSearch"
                    android:layout_width="26dp"
                    android:layout_height="26dp"
                    android:src="@drawable/ic_search"
                    app:tint="#333333" />
            </LinearLayout>

            <!-- Search Bar -->
            <LinearLayout
                android:layout_width="match_parent"
                android:layout_height="50dp"
                android:layout_marginStart="16dp"
                android:layout_marginEnd="16dp"
                android:layout_marginBottom="16dp"
                android:background="@drawable/bg_search"
                android:gravity="center_vertical"
                android:orientation="horizontal"
                android:paddingStart="16dp"
                android:paddingEnd="16dp"
                android:elevation="2dp">

                <EditText
                    android:id="@+id/etSearch"
                    android:layout_width="0dp"
                    android:layout_height="match_parent"
                    android:layout_weight="1"
                    android:background="@null"
                    android:hint="Search for stores, deals &amp; coupons..."
                    android:textColorHint="@color/text_hint"
                    android:textColor="#333333"
                    android:textSize="14sp"
                    android:singleLine="true"
                    android:imeOptions="actionSearch" />

                <ImageView
                    android:id="@+id/ivSearchIcon"
                    android:layout_width="22dp"
                    android:layout_height="22dp"
                    android:src="@drawable/ic_search"
                    app:tint="#E91E63" />
            </LinearLayout>

            <!-- ===== BANNER SECTION ===== -->
            <androidx.viewpager2.widget.ViewPager2
                android:id="@+id/vpBanner"
                android:layout_width="match_parent"
                android:layout_height="160dp"
                android:layout_marginStart="16dp"
                android:layout_marginEnd="16dp"
                android:layout_marginBottom="16dp"
                android:background="@drawable/bg_store_card"
                android:clipToOutline="true" />

            <!-- ===== STORES (Horizontal) ===== -->
            <androidx.recyclerview.widget.RecyclerView
                android:id="@+id/rvStores"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:clipToPadding="false"
                android:paddingStart="12dp"
                android:paddingEnd="12dp"
                android:layout_marginBottom="16dp"/>

            <!-- ===== TOP COUPONS ===== -->
            <LinearLayout
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:orientation="horizontal"
                android:gravity="center_vertical"
                android:paddingStart="16dp"
                android:paddingEnd="16dp"
                android:layout_marginBottom="8dp">

                <TextView
                    android:layout_width="0dp"
                    android:layout_height="wrap_content"
                    android:layout_weight="1"
                    android:text="Top Coupons for You"
                    android:textColor="#333333"
                    android:textSize="16sp"
                    android:textStyle="bold" />

                <TextView
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:text="View All"
                    android:textColor="#E91E63"
                    android:textSize="14sp" />
            </LinearLayout>

            <androidx.recyclerview.widget.RecyclerView
                android:id="@+id/rvTopCoupons"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:nestedScrollingEnabled="false"
                android:paddingStart="8dp"
                android:paddingEnd="8dp"
                android:layout_marginBottom="16dp"/>

            <!-- ===== BEST DEALS ===== -->
            <LinearLayout
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:orientation="horizontal"
                android:gravity="center_vertical"
                android:paddingStart="16dp"
                android:paddingEnd="16dp"
                android:layout_marginBottom="8dp">

                <TextView
                    android:layout_width="0dp"
                    android:layout_height="wrap_content"
                    android:layout_weight="1"
                    android:text="Today's Best Deals"
                    android:textColor="#333333"
                    android:textSize="16sp"
                    android:textStyle="bold" />

                <TextView
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:text="View All"
                    android:textColor="#E91E63"
                    android:textSize="14sp" />
            </LinearLayout>

            <androidx.recyclerview.widget.RecyclerView
                android:id="@+id/rvBestDeals"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:clipToPadding="false"
                android:paddingStart="12dp"
                android:paddingEnd="12dp"/>

        </LinearLayout>
    </androidx.core.widget.NestedScrollView>
</RelativeLayout>
""")
