# Quality checks derived from earlier campaign fixes

- Use inline SVG for arrows, controls and markers; test Safari/iOS rather than assuming desktop characters render identically.
- Inspect width AND rendered height of every mobile image; fixed intrinsic height can leave a huge image without horizontal overflow. Images must preserve intentional crops at 320, 375, 390 and 430px.
- Check headline wraps, line height, consistent spacing, button targets, navigation, footer and every language. No clipped text or sideways scrolling.
- View generated people at native size; inspect anatomy, garment details and identity consistency. Do not describe sample still checks as full video/motion approval.
- Disable animation under reduced-motion settings; keyboard navigation and visible focus must work.
- Read the actual CTA URL and registration response. A deployment success or screenshot is not proof that a form submits.
- Block analytics tags until opt-in; test decline, accept, preferences and withdrawal. Never embed API secrets or customer lists.
- UTM parameters survive CTA navigation, preserve non-UTM query parameters and never contain personal information.
- Test the actual deployed mobile page after publishing. Distinguish local verification from live-host verification.
