# AGENTS.md — React Native

React Native-specific rules for this codebase. Overrides global `~/AGENTS.md`.

> This file contains only React Native-specific conventions. Do not repeat generic global rules here unless they need a stricter or more concrete React Native interpretation.

---

## TYPESCRIPT

- MUST avoid `any`; use `unknown` and narrow it properly.
- MUST document unavoidable `any` usage with a short reason.
- MUST type function parameters and return values explicitly when the type is not obvious from local inference.
- MUST handle `null` and `undefined` intentionally.
- MUST prefer `type` for object shapes; use `interface` only when extension or declaration merging is needed.
- SHOULD avoid non-null assertions (`!`).
- SHOULD avoid `as` casting unless there is no safer alternative.
- SHOULD keep types close to the feature that owns them.
- SHOULD extract shared types only after reuse is proven.

---

## QUALITY

- MUST prioritize quality code over merely working code: keep changes maintainable, reusable, typed, tokenized, and verified instead of stopping at the first functional result.
- MUST keep source files at or below 300 lines unless the file is generated, declarative config, or a clearly justified exception.
- MUST run `npm run check:lines` after source refactors to verify the 300-line file limit when the script exists.
- MUST remove obvious duplication during related edits by extracting shared components or utilities when reuse is already proven.
- MUST keep changes scoped to the requested behavior unless a small related refactor clearly improves correctness or maintainability.
- SHOULD prefer small, behavior-preserving refactors that improve clarity without broad rewrites.
- SHOULD avoid clever abstractions before a real reuse pattern exists.

---

## TOOLCHAIN

- MUST use Expo as the default toolchain unless the project explicitly requires bare React Native.
- MUST keep project configuration aligned with the chosen toolchain.
- SHOULD prefer Expo-supported libraries before adding custom native complexity.
- SHOULD document clearly when the project cannot use Expo defaults.
- SHOULD avoid adding native modules unless the feature requires them and the tradeoff is documented.

---

## PROJECT STRUCTURE

- MUST group code by feature, not by technical type.
- MUST keep navigation or routing code in a dedicated `@/navigation`, `@/routes`, or Expo Router app structure.
- MUST use absolute imports with the `@/` alias.
- MUST name files after what they export.
- SHOULD keep one component per file.
- SHOULD keep components small and focused.
- SHOULD keep feature-specific logic inside the feature until reuse is proven.
- SHOULD move shared business logic into hooks, services, or `@/lib` instead of UI components.
- SHOULD keep API clients, storage helpers, analytics, and other cross-cutting utilities outside screen components.

---

## NAMING

- MUST use PascalCase for components, screens, and types.
- MUST use camelCase for variables and functions.
- MUST use UPPER_SNAKE_CASE for constants.
- MUST prefix boolean variables with `is`, `has`, or `can`.
- MUST suffix screen components with `Screen` when the project uses screen components directly.
- SHOULD use kebab-case for folders and non-component file names when the project convention follows it.
- SHOULD keep naming consistent across each feature.
- SHOULD name handlers by intent, for example `handleSubmit`, `handleRetry`, or `handleClose`.

---

## PLATFORM

- MUST assume iOS and Android can behave differently.
- MUST isolate platform-specific behavior with `Platform.OS`, `Platform.select()`, or platform-specific files when needed.
- MUST keep platform-sensitive behavior explicit and localized.
- SHOULD extract repeated platform branching into shared utilities.
- SHOULD avoid spreading platform conditionals across unrelated files.
- SHOULD verify behavior on both platforms when touching keyboard, gestures, navigation, safe areas, permissions, or native modules.

---

## STYLING

- MUST use a shared design token or theme system for colors, spacing, typography, and radius values.
- MUST NOT hardcode color values in components; use semantic design tokens whose names match the UI use case.
- MUST create or choose the closest semantic token automatically when no existing token represents the use case.
- MUST name style variables and tokens by use case, not by incidental color value.
- MUST deduplicate semantic tokens when multiple variables share the same use case and color value; consolidate by reusing the best existing token or creating a clearer shared token and migrating old references.
- MUST prefer `StyleSheet.create()` for static and reusable styles.
- MUST use flexbox as the default layout system.
- SHOULD avoid deeply nested `View` hierarchies when a flatter layout is clearer.
- SHOULD allow small inline styles only for simple dynamic values that do not belong in shared styles.
- SHOULD use fixed spacing tokens by default and use screen dimensions only when layout truly depends on screen size.
- SHOULD avoid magic numbers unless they are documented or clearly tied to a platform requirement.

---

## ACCESSIBILITY

- MUST provide accessible labels for interactive elements without visible text.
- MUST use appropriate accessibility roles for buttons, links, inputs, tabs, and toggles.
- MUST ensure touch targets are large enough for mobile use.
- MUST preserve readable text contrast through design tokens.
- MUST keep screen reader order logical and predictable.
- SHOULD provide accessibility hints when the action is not obvious from the label.
- SHOULD expose selected, disabled, expanded, and loading states to assistive technologies where relevant.

---

## SAFE AREA

- MUST handle safe areas on all root screens.
- MUST use `react-native-safe-area-context`.
- MUST avoid hardcoded padding meant to simulate safe area behavior.
- SHOULD use `useSafeAreaInsets()` when screen layout needs custom safe area control.
- SHOULD keep safe area handling close to the screen boundary.
- SHOULD verify safe area behavior on devices with notches, home indicators, and different status bar heights.

---

## COMPONENTS

- MUST keep components focused on presentation and interaction.
- MUST keep side effects out of render logic.
- MUST prefer composition over prop-heavy mega components.
- MUST reuse existing components completely: match both visual styling and interaction behavior unless a deliberate, documented variant is required.
- MUST keep reusable component styling locked to the design system; callers may vary component presence/slots only, not override core visual styling.
- MUST wrap critical screen trees with error boundaries to prevent full-app crashes.
- MUST show a fallback UI instead of a white screen when a render error occurs.
- SHOULD extract reusable UI only after a clear reuse pattern exists.
- SHOULD split components when they start handling too many responsibilities.
- SHOULD check existing shared components, hooks, and utilities before introducing new React Native-specific abstractions.
- SHOULD keep loading, empty, error, and success states explicit.

---

## LISTS AND IMAGES

- MUST use `FlatList` or `FlashList` for long or dynamic lists.
- MUST avoid rendering large collections with `ScrollView` plus `.map()`.
- MUST use stable keys for list items.
- MUST use a caching-aware image solution for remote images.
- MUST provide stable image sizing behavior to avoid layout jumps.
- SHOULD use `expo-image` for remote images in Expo-based projects unless there is a documented reason not to.
- SHOULD use placeholders, content fit, and caching intentionally.
- SHOULD avoid unoptimized remote image rendering in scrolling screens.
- SHOULD memoize expensive list item rendering only when there is a measured or obvious performance reason.

---

## NAVIGATION

- MUST use React Navigation or Expo Router consistently.
- MUST document the navigation choice early and keep routing conventions consistent.
- MUST type route params explicitly using a shared param list pattern when using React Navigation directly.
- MUST pass only serializable navigation params.
- MUST use the navigation or router API for screen transitions.
- SHOULD prefer Expo Router for Expo apps when file-based routing, deep linking, or web support is important.
- SHOULD use `navigate()` for normal flows and `replace()` when back navigation should not return to the previous screen.
- SHOULD keep reusable navigation logic in helpers or hooks instead of scattering it across screens.
- SHOULD handle unsaved changes explicitly before allowing destructive back navigation.
- SHOULD keep deep linking behavior in mind when adding or changing routes.

---

## FORMS AND KEYBOARD

- MUST handle keyboard overlap for input-heavy screens.
- MUST dismiss the keyboard intentionally when the UX calls for it.
- MUST use `keyboardShouldPersistTaps="handled"` on scrollable forms containing inputs.
- MUST keep form state and validation predictable and explicit.
- SHOULD use `KeyboardAvoidingView` where it improves usability.
- SHOULD use `KeyboardAwareScrollView` or equivalent for complex input-heavy screens when `KeyboardAvoidingView` is not sufficient.
- SHOULD use platform-appropriate keyboard behavior instead of forcing identical behavior on iOS and Android.
- SHOULD avoid hiding validation errors behind the keyboard.
- SHOULD keep submit buttons reachable while the keyboard is open when the form UX requires it.

---

## STATE AND MEMORY

- MUST clean up subscriptions, timers, and listeners in `useEffect`.
- MUST prevent state updates after a component unmounts.
- MUST keep state minimal and derive values when possible.
- MUST keep server state, local UI state, and persistent storage state conceptually separate.
- SHOULD cancel or ignore outdated async work during cleanup.
- SHOULD avoid storing large derived objects in component state.
- SHOULD avoid duplicating props into state unless the component intentionally needs a local draft.

---

## NETWORK

- MUST handle offline-aware UX when the feature depends on network access.
- MUST show meaningful UI when a network request fails.
- MUST set request timeout or cancellation behavior.
- MUST avoid duplicating fetch logic across screens.
- SHOULD detect connectivity changes when the feature depends on live network availability.
- SHOULD centralize API clients and request behavior instead of duplicating fetch logic.
- SHOULD retry only when the operation is safe to retry.
- SHOULD separate request, transform, and presentation logic when the flow becomes complex.

---

## CLIENT SECURITY

- MUST never store secrets, tokens, or sensitive credentials in plain `AsyncStorage`.
- MUST use secure storage for sensitive client-side values.
- MUST avoid logging tokens, secrets, authorization headers, personal data, or sensitive payloads.
- MUST keep environment-specific values out of committed source files unless they are explicitly public.
- SHOULD keep sensitive logic on the server whenever possible.
- SHOULD minimize the amount of sensitive data stored on device.
- SHOULD validate security-sensitive assumptions at API boundaries, not only in the client.

---

## PERMISSIONS

- MUST request permissions only when the user action requires them.
- MUST explain permission-dependent UX clearly before or during the request flow.
- MUST handle denied, blocked, unavailable, and limited permission states.
- SHOULD avoid requesting multiple unrelated permissions at once.
- SHOULD keep permission logic centralized when used across multiple features.

---

## PERFORMANCE

- MUST avoid unnecessary re-renders in frequently updated or list-heavy screens.
- MUST avoid expensive synchronous work during render.
- MUST keep animations smooth by avoiding JS-thread-heavy work during interactions.
- SHOULD use memoization only when it solves a real render or calculation problem.
- SHOULD defer non-critical work until after initial screen render when possible.
- SHOULD prefer native-driven or optimized animation libraries for complex animations.

---

## TESTING

- MUST add or update tests for critical business logic when behavior changes.
- MUST keep tests focused on observable behavior, not implementation details.
- MUST cover important loading, error, empty, and success states when practical.
- SHOULD test hooks, utilities, and data transformations separately from UI when they contain meaningful logic.
- SHOULD avoid brittle snapshot tests for complex screens unless snapshots provide clear value.

---

## REACT NATIVE VERIFICATION

- MUST verify platform-sensitive flows on both iOS and Android before shipping.
- MUST verify critical UI, navigation, keyboard, gesture, and safe-area behavior after meaningful changes.
- MUST verify loading, empty, error, and offline states for network-dependent features.
- SHOULD test on realistic device sizes when layout or interaction behavior is sensitive to screen dimensions.
- SHOULD treat warnings that indicate real runtime or platform risk as problems to resolve.
- SHOULD run the project’s lint, typecheck, test, and relevant Expo or React Native checks before finalizing substantial changes.

---

## DYNAMIC RULES

- MUST update this file when user instructions conflict with existing rules and the new behavior is better.
- MUST NOT ignore recurring patterns that should become rules.
- MUST keep updates minimal and actionable.
- MUST NOT add vague, redundant, or one-off rules.
- MUST remove or revise rules that become harmful, obsolete, or inconsistent with the project.
