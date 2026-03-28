# AGENTS.md — React Native

React Native-specific rules for this codebase. Overrides global `~/AGENTS.md`.

> This file contains only React Native-specific conventions. Do not repeat generic global rules here unless they need a stricter or more concrete React Native interpretation.

---

## TYPESCRIPT

- MUST never use `any`; use `unknown` and narrow it properly.
- MUST type function parameters and return values explicitly.
- MUST handle `null` and `undefined` intentionally.
- MUST prefer `type` for object shapes; use `interface` only when extension or declaration merging is needed.
- SHOULD avoid non-null assertions (`!`).
- SHOULD avoid `as` casting unless there is no safer alternative.
- SHOULD keep types close to the feature that owns them.

---

## TOOLCHAIN

- MUST use **Expo** as the default toolchain unless the project explicitly requires bare React Native.
- MUST keep project configuration aligned with the chosen toolchain.
- SHOULD prefer Expo-supported libraries before adding custom native complexity.
- SHOULD document clearly when the project cannot use Expo defaults.

---

## PROJECT STRUCTURE

- MUST group code by feature, not by technical type.
- MUST keep navigation code in a dedicated `@/navigation` area.
- MUST use absolute imports with the `@/` alias.
- MUST name files after what they export.
- SHOULD keep one component per file.
- SHOULD keep components small and focused.
- SHOULD keep feature-specific logic inside the feature until reuse is proven.
- SHOULD move shared business logic into hooks, services, or `@/lib` instead of UI components.

---

## NAMING

- MUST use PascalCase for components, screens, and types.
- MUST use camelCase for variables and functions.
- MUST use UPPER_SNAKE_CASE for constants.
- MUST prefix boolean variables with `is`, `has`, or `can`.
- MUST suffix screen components with `Screen`.
- SHOULD use kebab-case for folders and non-component file names when the project convention follows it.
- SHOULD keep naming consistent across each feature.

---

## PLATFORM

- MUST assume iOS and Android can behave differently.
- MUST isolate platform-specific behavior with `Platform.OS`, `Platform.select()`, or platform-specific files when needed.
- MUST keep platform-sensitive behavior explicit and localized.
- SHOULD extract repeated platform branching into shared utilities.
- SHOULD avoid spreading platform conditionals across unrelated files.

---

## STYLING

- MUST use a shared design token or theme system for colors, spacing, typography, and radius values.
- MUST prefer `StyleSheet.create()` for static and reusable styles.
- MUST use flexbox as the default layout system.
- SHOULD avoid deeply nested `View` hierarchies when a flatter layout is clearer.
- SHOULD allow small inline styles only for simple dynamic values that do not belong in shared styles.
- SHOULD use fixed spacing tokens by default and use screen dimensions only when layout truly depends on screen size.

---

## SAFE AREA

- MUST handle safe areas on all root screens.
- MUST use `react-native-safe-area-context`.
- MUST avoid hardcoded padding meant to simulate safe area behavior.
- SHOULD use `useSafeAreaInsets()` when screen layout needs custom safe area control.
- SHOULD keep safe area handling close to the screen boundary.

---

## COMPONENTS

- MUST keep components focused on presentation and interaction.
- MUST keep side effects out of render logic.
- MUST prefer composition over prop-heavy mega components.
- SHOULD extract reusable UI only after a clear reuse pattern exists.
- SHOULD split components when they start handling too many responsibilities.
- SHOULD check existing shared components, hooks, and utilities before introducing new React Native-specific abstractions.
- MUST wrap critical screen trees with error boundaries to prevent full-app crashes.
- MUST show a fallback UI instead of a white screen when a render error occurs.

---

## LISTS AND IMAGES

- MUST use `FlatList` or `FlashList` for long or dynamic lists.
- MUST avoid rendering large collections with `ScrollView` plus `.map()`.
- MUST use a caching-aware image solution for remote images.
- MUST provide stable image sizing behavior to avoid layout jumps.
- SHOULD use `expo-image` for remote images in Expo-based projects unless there is a documented reason not to.
- SHOULD use placeholders, content fit, and caching intentionally.
- SHOULD avoid unoptimized remote image rendering in scrolling screens.

---

## NAVIGATION

- MUST use **React Navigation** conventions consistently.
- MUST type route params explicitly using a shared param list pattern.
- MUST pass only serializable navigation params.
- MUST use the navigation API for screen transitions.
- SHOULD use `navigate()` for normal flows and `replace()` when back navigation should not return to the previous screen.
- SHOULD keep reusable navigation logic in helpers or hooks instead of scattering it across screens.
- SHOULD handle unsaved changes explicitly before allowing destructive back navigation.

---

## FORMS AND KEYBOARD

- MUST handle keyboard overlap for input-heavy screens.
- MUST dismiss the keyboard intentionally when the UX calls for it.
- MUST use `keyboardShouldPersistTaps="handled"` on scrollable forms containing inputs.
- SHOULD use `KeyboardAvoidingView` where it improves usability.
- SHOULD use platform-appropriate keyboard behavior instead of forcing identical behavior on iOS and Android.
- SHOULD keep form state and validation predictable and explicit.

---

## STATE AND MEMORY

- MUST clean up subscriptions, timers, and listeners in `useEffect`.
- MUST prevent state updates after a component unmounts.
- MUST keep state minimal and derive values when possible.
- SHOULD cancel or ignore outdated async work during cleanup.
- SHOULD avoid storing large derived objects in component state.

---

## NETWORK

- MUST handle offline-aware UX when the feature depends on network access.
- MUST show meaningful UI when a network request fails.
- MUST set request timeout or cancellation behavior.
- SHOULD detect connectivity changes when the feature depends on live network availability.
- SHOULD centralize API clients and request behavior instead of duplicating fetch logic.
- SHOULD retry only when the operation is safe to retry.

---

## CLIENT SECURITY

- MUST never store secrets, tokens, or sensitive credentials in plain `AsyncStorage`.
- MUST use secure storage for sensitive client-side values.
- SHOULD keep sensitive logic on the server whenever possible.
- SHOULD minimize the amount of sensitive data stored on device.

---

## REACT NATIVE VERIFICATION

- MUST verify platform-sensitive flows on both iOS and Android before shipping.
- MUST verify critical UI, navigation, keyboard, gesture, and safe-area behavior after meaningful changes.
- SHOULD test on realistic device sizes when layout or interaction behavior is sensitive to screen dimensions.
- SHOULD treat warnings that indicate real runtime or platform risk as problems to resolve.

---

## DYNAMIC RULES

- MUST update this file when user instructions conflict with existing rules and the new behavior is better.
- MUST NOT ignore recurring patterns that should become rules.
- MUST keep updates minimal and actionable.
- MUST NOT add vague, redundant, or one-off rules.