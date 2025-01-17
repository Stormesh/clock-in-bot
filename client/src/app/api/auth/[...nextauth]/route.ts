//Auth.js
import { handlers } from "@/src/auth"; // Referring to the auth.ts we just created
export const { GET, POST } = handlers;

//Better Auth
// import { auth } from "@/src/auth";
// import { toNextJsHandler } from "better-auth/next-js";

// export const { POST, GET } = toNextJsHandler(auth);
