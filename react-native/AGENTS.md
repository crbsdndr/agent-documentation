# AGENTS.md — React Native

React Native-specific rules for this codebase. Overrides global `~/AGENTS.md`.

> This file is **living documentation** — rules here can and should evolve over time. When a user's request conflicts with an existing rule, discuss the conflict, and if needed, update this file to reflect the new convention. When refactoring or improving the codebase reveals a bad pattern, **proactively add or update the relevant rule** here so it doesn't happen again.

---

## TYPESCRIPT RULES

- Never use `any` — use `unknown` and narrow the type if needed.
- Avoid non-null assertions (`!`) — handle nullability explicitly.
- Always type function return values explicitly.
- Use `type` for object shapes, `interface` only when extending.
- Never cast with `as` unless absolutely necessary.

## FRAMEWORK RULES

- Use **Expo** as the default toolchain unless the project explicitly uses bare React Native.
- Use **React Navigation** for routing — follow its stack, tab, and drawer navigator conventions.
- Never use `index.js` as a component file — name files after what they export.
- Prefer **named exports** over default exports, except for screens.
- Use **absolute imports** with `@/` alias.

## PLATFORM RULES

- Never assume iOS and Android behave the same — always test both.
- Use `Platform.OS` to handle platform-specific logic, or `.ios.tsx` / `.android.tsx` file extensions for platform-specific components.
- Use `Platform.select()` for platform-specific styles.
- Never hardcode pixel values — use `Dimensions` or responsive utilities.

## NAMING CONVENTION

- **Components & Screens** → PascalCase (`UserCard.tsx`, `HomeScreen.tsx`)
- **Files & folders** → kebab-case (`user-card.tsx`, `auth-utils.ts`)
- **Variables & functions** → camelCase (`getUserData`)
- **Constants** → UPPER_SNAKE_CASE (`MAX_RETRY_COUNT`)
- **Types & interfaces** → PascalCase (`UserProps`)
- **Boolean variables** → prefix with `is`, `has`, or `can` (`isLoading`, `hasError`)
- **Screens** → suffix with `Screen` (`HomeScreen`, `ProfileScreen`)

## MODULARITY RULES

- One component per file — no multiple component exports in a single file.
- Keep components **small and focused** — if it does more than one thing, split it.
- Separate concerns: UI logic stays in components, business logic goes to `@/lib` or `@/hooks`.
- Group by feature, not by type — `@/features/auth/` instead of `@/screens/` + `@/components/`.

## REUSE RULES

- Before building a new component, **check `@/components`** first.
- Before writing a utility function, **check `@/lib`** first.
- Extract repeated logic (3+ usages) into a shared hook or utility.

## STYLING RULES

- Always use `StyleSheet.create()` — never use inline style objects.
- Never hardcode colors — use a theme/token system (`@/theme/colors`).
- Avoid deeply nested `View` components — flatten layout where possible.
- Use `flex` for layout — avoid fixed widths/heights unless necessary.

## PERFORMANCE RULES

- Use `FlatList` or `FlashList` for long lists — never use `ScrollView` with `.map()`.
- Memoize expensive components with `React.memo` and callbacks with `useCallback`.
- Avoid anonymous functions in JSX — define them outside render.
- Images must use a caching-aware library (e.g. `expo-image`) — never raw `<Image>` for remote URLs.

## SECURITY RULES

- Never store sensitive data (tokens, passwords) in `AsyncStorage` — use `expo-secure-store`.
- Always validate and sanitize user input before processing.
- Never expose API keys in the codebase — use environment variables via `expo-constants`.

## ERROR HANDLING RULES

- Always wrap navigation actions in try/catch.
- Use an **error boundary** at the root level to catch unexpected crashes.
- Never let unhandled promise rejections fail silently.

## VERIFICATION RULES

- After changes, always verify using the project's available scripts:
  - Lint — check for linting errors
  - Typecheck — verify no TypeScript errors
  - Run on both iOS and Android simulators before shipping

## SAFE AREA RULES

- Always wrap root screens with `SafeAreaView` or use `useSafeAreaInsets()` — never ignore notch, status bar, or bottom gesture area.
- Never hardcode top/bottom padding to compensate for safe area — use `react-native-safe-area-context` instead.

## KEYBOARD RULES

- Always wrap forms with `KeyboardAvoidingView` — behavior `padding` for iOS, `height` for Android.
- Always handle keyboard dismiss on outside tap using `Keyboard.dismiss()`.
- Use `keyboardShouldPersistTaps="handled"` on `ScrollView` that contains inputs.

## ANIMATION RULES

- Use **react-native-reanimated** over the built-in `Animated` API — it runs on the UI thread and is significantly more performant.
- Use **react-native-gesture-handler** for gesture-based interactions — never use built-in `PanResponder`.
- Keep animations declarative with `useAnimatedStyle` and `useSharedValue`.
- Never block the JS thread with heavy computations during animations.

## NAVIGATION RULES

- Use **React Navigation** — follow its stack, tab, and drawer navigator conventions.
- Always type your navigation params using `RootStackParamList` pattern.
- Never pass non-serializable values (functions, class instances) as navigation params.
- Use `navigation.navigate()` for moving between screens, `navigation.replace()` when back navigation doesn't make sense (e.g. after login).
- Keep navigation logic out of components — use a dedicated `@/navigation` folder.

## ACCESSIBILITY RULES

- Every touchable element must have an `accessibilityLabel`.
- Use `accessibilityRole` to describe the purpose of interactive elements (`button`, `link`, etc).
- Never rely solely on color to convey information — always pair with text or icon.

## ANIMATION RULES

- Use **react-native-reanimated** over the built-in `Animated` API — it runs on the UI thread and is significantly more performant.
- Never block the JS thread with animations — always use `useSharedValue` and `useAnimatedStyle`.
- Keep animations subtle and purposeful — don't animate just for the sake of it.

## NAVIGATION RULES

- Always type route params — never pass untyped `params`.
- Never navigate by mutating state — always use the navigation API (`navigation.navigate`, `navigation.push`, etc).
- Keep navigation logic out of components — abstract into a navigation service or hook when reused.
- Always handle the back action explicitly on screens that have unsaved changes.

## MEMORY RULES

- Always return a cleanup function from `useEffect` when subscribing to events, timers, or listeners.
- Never update state on an unmounted component — cancel async operations on cleanup.
- Avoid storing large objects in state — keep state minimal and derive what you can.

## GESTURE RULES

- Always use **react-native-gesture-handler** touchables (`TouchableOpacity`, `Pressable`) — never use the ones from `react-native` core in screens with navigation.
- Wrap the root app with `GestureHandlerRootView`.
- Never nest multiple swipeable/gesture components without explicit gesture priority handling.

## NETWORK RULES

- Always handle offline state — never assume the user has a connection.
- Always show a meaningful UI when a network request fails — never fail silently.
- Use `@react-native-community/netinfo` to detect connectivity changes.
- Always set request timeouts — never let requests hang indefinitely.