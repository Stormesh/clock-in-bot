"use client";

import React, { FormEvent, useState } from "react";
import InputField from "@components/InputField";
import { useRouter } from "next/navigation";
import { signIn } from "next-auth/react";
import { signInSchema } from "../../lib/zod";

const Login = () => {
  const [error, setError] = useState<string>("");

  const router = useRouter();

  const handleFormSubmit = async (event: FormEvent) => {
    event.preventDefault();

    try {
      const formData = new FormData(event.target as HTMLFormElement);

      const user = {
        username: formData.get("username") as string,
        password: formData.get("password") as string,
      };

      const validation = await signInSchema.safeParseAsync(user);

      if (!validation.success)
        throw new Error(validation.error.errors.map((error) => error.message).join("\n"));

      // Auth.js
      const response = await signIn("credentials", {
        username: user.username,
        password: user.password,
        redirect: false,
      });

      if (response?.error || !response?.ok) {
        throw new Error("Failed to log in");
      }

      return router.push("/");
    } catch (e) {
      console.error(e);
      setError(e instanceof Error ? e.message : "Failed to log in");
    }
  };

  return (
    <div className="flex items-center justify-center h-screen">
      <form
        onSubmit={handleFormSubmit}
        className="flex flex-col justify-center items-center place-self-center rounded-lg bg-card-bg p-5 text-white"
      >
        <h1 className="text-3xl mb-3 font-bold">Enter your details</h1>
        <InputField
          name="username"
          labelText="Username"
          placeholder="Username"
          grid
          type="text"
        />
        <InputField
          name="password"
          labelText="Password"
          placeholder="Password"
          grid
          type="password"
        />
        {error && <h4 className="text-xl text-red-500 whitespace-pre-line text-center">{error}</h4>}
        <button
          className="bg-green-700 hover:bg-green-500 font-sans p-2 text-xl m-3 rounded-lg hover:scale-110 transition-all duration-300 cursor-pointer"
          type="submit"
        >
          Login
        </button>
      </form>
    </div>
  );
};

export default Login;
