package com.onlineshoppingapps

import android.content.ContentValues
import android.content.Context
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.net.Uri
import android.os.Build
import android.provider.MediaStore
import android.widget.Toast
import java.io.OutputStream

object GalleryUtils {

    fun saveTextToGallery(context: Context, title: String, text: String) {
        try {
            // 1. Create a Bitmap from the text
            val bitmap = Bitmap.createBitmap(500, 300, Bitmap.Config.ARGB_8888)
            val canvas = Canvas(bitmap)
            canvas.drawColor(Color.WHITE)
            
            val paint = Paint().apply {
                color = Color.BLACK
                textSize = 40f
                isAntiAlias = true
            }
            
            canvas.drawText(title, 50f, 100f, paint)
            paint.textSize = 30f
            canvas.drawText(text, 50f, 200f, paint)

            // 2. Save to MediaStore
            val filename = "${title}_${System.currentTimeMillis()}.jpg"
            var outputStream: OutputStream? = null
            
            val contentValues = ContentValues().apply {
                put(MediaStore.MediaColumns.DISPLAY_NAME, filename)
                put(MediaStore.MediaColumns.MIME_TYPE, "image/jpeg")
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                    put(MediaStore.MediaColumns.RELATIVE_PATH, "Pictures/SaveKaro")
                }
            }

            val imageUri: Uri? = context.contentResolver.insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, contentValues)
            
            if (imageUri != null) {
                outputStream = context.contentResolver.openOutputStream(imageUri)
                bitmap.compress(Bitmap.CompressFormat.JPEG, 100, outputStream!!)
                outputStream.close()
                Toast.makeText(context, "Saved to Gallery: $filename", Toast.LENGTH_SHORT).show()
            }
            
            bitmap.recycle()
        } catch (e: Exception) {
            Toast.makeText(context, "Failed to save: ${e.message}", Toast.LENGTH_SHORT).show()
            e.printStackTrace()
        }
    }
}
