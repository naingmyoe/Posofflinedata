# R8 / ProGuard Security & Obfuscation Rules for UN POS

# Enable Optimization and Repackaging for stronger obfuscation
-repackageclasses ''
-allowaccessmodification
-dontusemixedcaseclassnames
-skipnonpubliclibraryclasses
-verbose

# Preserve line numbers for stack traces while hiding original source file names
-keepattributes SourceFile,LineNumberTable,*Annotation*,Signature,InnerClasses,EnclosingMethod
-renamesourcefileattribute 'SourceFile'

# Keep Security Manager and Security Utils
-keep class com.example.security.** { *; }

# Keep Android Entry Points
-keep public class * extends android.app.Activity
-keep public class * extends android.app.Application
-keep public class * extends android.app.Service
-keep public class * extends android.content.BroadcastReceiver
-keep public class * extends android.content.ContentProvider

# Keep Jetpack Compose
-keep class androidx.compose.** { *; }
-keepclassmembers class * {
    @androidx.compose.runtime.Composable *;
}

# Keep Room Entities & DAOs
-keepclassmembers class * {
    @androidx.room.* *;
}
-keep @androidx.room.Entity class * { *; }
-keep @androidx.room.Dao interface * { *; }
-keep class * extends androidx.room.RoomDatabase { *; }

# Keep ViewModels
-keep class * extends androidx.lifecycle.ViewModel { *; }

# Keep Data Models & Moshi/Gson
-keepclassmembers class com.example.data.** { *; }
-keep class com.example.data.** { *; }

# Coroutines
-keepclassmembers class kotlinx.coroutines.** { *; }

# Prevent native method stripping
-keepclasseswithmembernames class * {
    native <methods>;
}

