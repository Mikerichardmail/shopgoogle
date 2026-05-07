import os

res_dir = r"f:\online shoping apps new\app\src\main\res"

def write_file(path, content):
    full_path = os.path.join(res_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"Created {path}")

write_file(r"drawable\bg_coupon_dashed.xml", """
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <stroke android:width="1dp" android:color="#E91E63" android:dashWidth="4dp" android:dashGap="4dp" />
    <solid android:color="#00FFFFFF"/>
    <corners android:radius="4dp" />
</shape>
""")

write_file(r"drawable\bg_btn_copy.xml", """
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <solid android:color="#E91E63" />
    <corners android:radius="6dp" />
</shape>
""")

write_file(r"drawable\ic_verified.xml", """
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="16dp" android:height="16dp" android:viewportWidth="24" android:viewportHeight="24">
    <path android:fillColor="#4CAF50" android:pathData="M12,2C6.48,2 2,6.48 2,12s4.48,10 10,10 10,-4.48 10,-10S17.52,2 12,2zM10,17l-5,-5 1.41,-1.41L10,14.17l7.59,-7.59L19,8l-9,9z"/>
</vector>
""")

write_file(r"layout\item_coupon.xml", """
<?xml version="1.0" encoding="utf-8"?>
<androidx.cardview.widget.CardView xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:layout_marginTop="6dp"
    android:layout_marginBottom="6dp"
    app:cardCornerRadius="12dp"
    app:cardElevation="0dp"
    app:cardBackgroundColor="#FFF8F8"> <!-- Default tint -->

    <androidx.constraintlayout.widget.ConstraintLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:padding="16dp">

        <!-- Store Logo & Name -->
        <LinearLayout
            android:id="@+id/llStoreInfo"
            android:layout_width="70dp"
            android:layout_height="wrap_content"
            android:orientation="vertical"
            android:gravity="center"
            app:layout_constraintStart_toStartOf="parent"
            app:layout_constraintTop_toTopOf="parent"
            app:layout_constraintBottom_toBottomOf="parent">

            <ImageView
                android:id="@+id/ivStoreLogo"
                android:layout_width="40dp"
                android:layout_height="40dp"
                android:src="@drawable/ic_launcher_foreground" />

            <TextView
                android:id="@+id/tvStoreName"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:layout_marginTop="4dp"
                android:text="Myntra"
                android:textColor="#333333"
                android:textSize="12sp"
                android:textStyle="bold"
                android:maxLines="1"/>
        </LinearLayout>

        <!-- Divider -->
        <View
            android:id="@+id/divider"
            android:layout_width="1dp"
            android:layout_height="0dp"
            android:background="#1A000000"
            android:layout_marginStart="12dp"
            app:layout_constraintStart_toEndOf="@id/llStoreInfo"
            app:layout_constraintTop_toTopOf="parent"
            app:layout_constraintBottom_toBottomOf="parent" />

        <!-- Coupon Details -->
        <LinearLayout
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:orientation="vertical"
            android:layout_marginStart="12dp"
            android:layout_marginEnd="8dp"
            app:layout_constraintStart_toEndOf="@id/divider"
            app:layout_constraintEnd_toStartOf="@id/llRightCol"
            app:layout_constraintTop_toTopOf="parent"
            app:layout_constraintBottom_toBottomOf="parent">

            <TextView
                android:id="@+id/tvCouponTitle"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="Flat ₹300 Off on ₹1999 &amp; Above"
                android:textColor="#333333"
                android:textSize="14sp"
                android:textStyle="bold"
                android:maxLines="2" />

            <LinearLayout
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:orientation="horizontal"
                android:gravity="center_vertical"
                android:layout_marginTop="6dp">

                <TextView
                    android:id="@+id/tvCategory"
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:text="Fashion"
                    android:textColor="#666666"
                    android:textSize="10sp" />

                <TextView
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:layout_marginStart="4dp"
                    android:layout_marginEnd="4dp"
                    android:text="•"
                    android:textColor="#666666"
                    android:textSize="10sp" />

                <ImageView
                    android:layout_width="12dp"
                    android:layout_height="12dp"
                    android:src="@drawable/ic_verified" />

                <TextView
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:layout_marginStart="4dp"
                    android:text="Verified Today"
                    android:textColor="#666666"
                    android:textSize="10sp" />
            </LinearLayout>
        </LinearLayout>

        <!-- Right Column (Code & Button) -->
        <LinearLayout
            android:id="@+id/llRightCol"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:orientation="vertical"
            android:gravity="end"
            app:layout_constraintEnd_toEndOf="parent"
            app:layout_constraintTop_toTopOf="parent"
            app:layout_constraintBottom_toBottomOf="parent">

            <!-- Code container -->
            <FrameLayout
                android:layout_width="90dp"
                android:layout_height="32dp"
                android:background="@drawable/bg_coupon_dashed"
                android:layout_marginBottom="8dp">
                
                <TextView
                    android:id="@+id/tvCode"
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:layout_gravity="center"
                    android:text="MYNTRA300"
                    android:textColor="#E91E63"
                    android:textSize="12sp"
                    android:textStyle="bold"
                    android:maxLines="1" />
            </FrameLayout>

            <Button
                android:id="@+id/btnCopy"
                android:layout_width="90dp"
                android:layout_height="36dp"
                android:background="@drawable/bg_btn_copy"
                android:text="Copy"
                android:textColor="#FFFFFF"
                android:textSize="13sp"
                android:textStyle="bold"
                android:insetTop="0dp"
                android:insetBottom="0dp"
                app:backgroundTint="#E91E63" />

            <TextView
                android:id="@+id/tvExpiry"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:layout_marginTop="6dp"
                android:text="Expires on 31 May 2025"
                android:textColor="#999999"
                android:textSize="9sp" />
        </LinearLayout>

    </androidx.constraintlayout.widget.ConstraintLayout>
</androidx.cardview.widget.CardView>
""")
