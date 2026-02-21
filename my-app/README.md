# 1. Setup Firebase Console

Open [console.firebase.google.com](console.firebase.google.com)

Create project

# 2. Create Authentication

Left sidebar -> Build -> Authentication

Create

Use Sign-in provider: `Email/Password`

Update [environment.ts](my-app/src/environments/environment.ts) (apiKey, authDomain, projectId, storageBucket, messagingSenderId, appId and measurementId if exist)

# 3. Create Realtime Database

Left sidebar -> Build -> Realtime Database

Create

Choose `europe-west1` location

Choose `Start in test mode`

Update [environment.ts](my-app/src/environments/environment.ts) (databaseURL)