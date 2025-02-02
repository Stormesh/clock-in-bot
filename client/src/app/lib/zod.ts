import { object, string } from "zod";

export const signInSchema = object({
  username: string({ required_error: "Username is required" }).regex(
    /^[a-zA-Z0-9_]+$/,
    "Username can only contain letters and numbers"
  ),
  password: string({ required_error: "Password is required" }).min(
    8,
    "Password must be at least 8 characters"
  ),
});

export const signUpSchema = signInSchema.extend({
  role: string({ required_error: "Role is required" }),
});
