# Google Authentication Guide for TableNow 🔐

This guide outlines the steps to integrate Google Sign-In into the TableNow Flutter app using **Supabase** and the **google_sign_in** package.

---

## 🚀 Two Ways to Implement
There are two main ways to implement Google Sign-In with Supabase in Flutter:

1.  **Native Sign-In (Recommended):** Uses the `google_sign_in` package for a smooth, native experience. 
2.  **Web OAuth Flow:** Opens an external browser or in-app web view for sign-in. Easy to set up but less smooth.

---

## 1. Google Cloud Console Setup ☁️

To allow users to sign in with Google, you need to create OAuth 2.0 Credentials in the [Google Cloud Console](https://console.cloud.google.com/).

### Step 1: Create a Project
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project named `TableNow`.

### Step 2: Configure OAuth Consent Screen
1. Navigate to **APIs & Services > OAuth consent screen**.
2. Select **External** and click **Create**.
3. Fill in the required app information:
   - **App name**: TableNow
   - **User support email**: Your email
   - **Developer contact info**: Your email
4. Add the `.../auth/userinfo.email` and `.../auth/userinfo.profile` scopes.

### Step 3: Create OAuth Client IDs

#### 📱 Android
1. Go to **APIs & Services > Credentials > Create Credentials > OAuth client ID**.
2. Select **Android**.
3. **Package name**: `com.example.tablenow_app`
4. **SHA-1 fingerprint**: Run `./gradlew signingReport` in the `android` folder.
5. Download the `google-services.json` and place it in `android/app/`.

#### 🍎 iOS
1. Click **Create Credentials > OAuth client ID**.
2. Select **iOS**.
3. **Bundle ID**: `com.example.tablenow_app`
4. Download the `GoogleService-Info.plist` and add it to your Xcode project under `Runner`.

#### 🌐 Web (Required for Supabase Backend)
1. Click **Create Credentials > OAuth client ID**.
2. Select **Web application**.
3. Add **Authorized redirect URIs**:
   - `https://hnanftiymngdrnxcaxus.supabase.co/auth/v1/callback`
4. Click **Create** and copy the **Client ID** and **Client Secret**.

---

## 2. Supabase Dashboard Configuration ⚡️

1. Go to your [Supabase Project Dashboard](https://supabase.com/dashboard).
2. Navigate to **Authentication > Providers**.
3. Enable **Google**.
4. Paste the **Client ID (Web)** and **Client Secret (Web)** from the Google Cloud Console.
5. Click **Save**.

---

## 3. Implementation (Native Flow) 🚀

Current code in `login_screen.dart` uses the Web Flow. To switch to the **Native Flow**, update the `_signInWithGoogle` method:

```dart
Future<void> _signInWithNativeGoogle() async {
  setState(() {
    _isGoogleLoading = true;
    _errorMessage = null;
  });

  try {
    // 1. Initialize Google Sign In
    const webClientId = 'YOUR_WEB_CLIENT_ID.apps.googleusercontent.com';
    const iosClientId = 'YOUR_IOS_CLIENT_ID.apps.googleusercontent.com';

    final GoogleSignIn googleSignIn = GoogleSignIn(
      clientId: iosClientId,
      serverClientId: webClientId,
    );
    
    // 2. Start the flow
    final googleUser = await googleSignIn.signIn();
    if (googleUser == null) return; // User canceled

    final googleAuth = await googleUser.authentication;
    final accessToken = googleAuth.accessToken;
    final idToken = googleAuth.idToken;

    if (idToken == null) {
      throw 'No ID Token found.';
    }

    // 3. Authenticate with Supabase
    await Supabase.instance.client.auth.signInWithIdToken(
      provider: OAuthProvider.google,
      idToken: idToken,
      accessToken: accessToken,
    );
  } catch (e) {
    setState(() {
      _errorMessage = "Native Google sign-in failed: $e";
    });
  } finally {
    if (mounted) {
      setState(() {
        _isGoogleLoading = false;
      });
    }
  }
}
```

---

## 🛠️ Platform Specifics

### iOS Checklist
- [ ] Add `GoogleService-Info.plist` to `ios/Runner/`.
- [ ] Add the following to `ios/Runner/Info.plist`:

```xml
<key>CFBundleURLTypes</key>
<array>
  <dict>
    <key>CFBundleTypeRole</key>
    <string>Editor</string>
    <key>CFBundleURLSchemes</key>
    <array>
      <string>com.googleusercontent.apps.YOUR_iOS_CLIENT_ID</string>
    </array>
  </dict>
</array>
```

### Android Checklist
- [ ] Add `google-services.json` to `android/app/`.
- [ ] Ensure the SHA-1 in Google Cloud Console matches your local build (Debug/Release).

---

> [!IMPORTANT]
> Never commit your `Client Secret` to public repositories. Use environment variables or secure storage and add secret files to `.gitignore`.
