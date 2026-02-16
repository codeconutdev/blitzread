# ZapRead - App Store Readiness Checklist

## Bundle & Identity
- [x] Bundle ID updated to `com.borgo.blitzread`
- [x] App icon set (lightning bolt B - already done)
- [x] Company: Borgo Technologies LLC (NJ)
- [ ] Apple Developer account ready
- [ ] App Store Connect app created

## Privacy & Legal
- [x] Privacy policy created (`privacy-policy.md`)
- [ ] Privacy policy hosted at public URL (required for App Store)
- [ ] Privacy manifest added (iOS 17+)
- [ ] Data collection disclosure completed in App Store Connect

## Marketing Assets
- [x] App Store screenshots generated (1290x2796 - 6.7")
- [ ] Additional screenshot sizes if needed:
  - [ ] 6.5" (1284x2778 - iPhone 14 Plus, 13 Pro Max, 12 Pro Max)
  - [ ] 5.5" (1242x2208 - iPhone 8 Plus, 7 Plus, 6s Plus)
- [x] App Store listing copy written (`store-listing.md`)
- [x] App name: **ZapRead**
- [x] Subtitle: "Speed Read Anything"
- [ ] App preview video (optional but recommended)

## App Store Metadata
- [x] Category: **Productivity**
- [x] Keywords: speed reading, RSVP, fast reader, reading trainer
- [x] Age rating: 4+ (no objectionable content)
- [ ] Support URL (can use GitHub repo or create landing page)
- [ ] Marketing URL (optional)

## Technical Requirements
- [ ] Tested on physical device (not just simulator)
- [ ] No crashes on launch ✓
- [ ] Handles empty state gracefully ✓
- [ ] Works offline ✓
- [ ] Handles interruptions (calls, notifications) ✓
- [ ] App Store build submitted via Xcode/Transporter
- [ ] All required device screenshots uploaded

## App Review Preparation
- [ ] Demo account (not needed - no login required)
- [ ] App Review notes explaining RSVP speed reading
- [ ] Contact information for Apple review team
- [ ] Test cases documented

## Post-Launch
- [ ] App Store optimization (ASO) - monitor keywords
- [ ] User feedback monitoring
- [ ] Analytics integration (if desired)
- [ ] Version 1.1 roadmap

---

## Notes

### Privacy Manifest (iOS 17+)
ZapRead doesn't use any required reason APIs, but Apple may require a privacy manifest. Create `ios/Runner/PrivacyInfo.xcprivacy` if submission fails:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>NSPrivacyTracking</key>
    <false/>
    <key>NSPrivacyCollectedDataTypes</key>
    <array/>
    <key>NSPrivacyAccessedAPITypes</key>
    <array/>
</dict>
</plist>
```

### Hosting Privacy Policy
Free options:
- GitHub Pages (use repo wiki or create docs/ folder)
- Notion (free page with public link)
- Google Docs (set to "Anyone with link can view")

### App Review Tips
- Emphasize: No account required, no data collection, 100% offline
- RSVP = Rapid Serial Visual Presentation (explain the technique)
- Mention smart ORP (Optimal Recognition Point) algorithm
- Show how to paste/type text and adjust WPM

### Build & Submit
```bash
# Clean build
cd ~/projects/speed-reader
flutter clean
flutter pub get

# Archive for App Store (requires Mac with Xcode)
flutter build ios --release

# Open in Xcode to archive & upload
open ios/Runner.xcworkspace
```

In Xcode:
1. Select "Any iOS Device" as target
2. Product → Archive
3. Upload to App Store Connect
4. Complete metadata in App Store Connect
5. Submit for review

---

**Bundle ID:** `com.borgo.blitzread`  
**Version:** 1.0.0 (Build 1)  
**Company:** Borgo Technologies LLC  
**Copyright:** © 2025 Borgo Technologies LLC
