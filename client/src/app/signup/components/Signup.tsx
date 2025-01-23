"use client";

import React, { useState } from "react";
import InputField from "../../login/components/InputField";
import Link from "next/link";

const Signup = () => {
  enum indicatorState {
    success = 1,
    error = 0,
    none = -1,
  }
  const [indicator, setIndicator] = useState(indicatorState.none);

  enum indicatorTextState {
    created = "Account created successfully!",
    createdFail = "Failed to process request",
    createdExists = "User already exists",
    missing = "Missing credentials",
  }
  const [indicatorText, setIndicatorText] = useState<
    string | indicatorTextState
  >(indicatorTextState.missing);

  const handleFormSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    try {
      const formData = new FormData(event.currentTarget);
      const response = await fetch("/api/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: formData.get("username"),
          password: formData.get("password"),
          role: formData.get("role"),
        }),
      });

      if (response.ok) {
        setIndicator(indicatorState.success);
        setIndicatorText(indicatorTextState.created);
      } else {
        setIndicator(indicatorState.error);
        if (response.status === 409) {
          setIndicatorText(indicatorTextState.createdExists);
        } else if (response.status === 400) {
          setIndicatorText(indicatorTextState.missing);
        } else {
          setIndicatorText(indicatorTextState.createdFail);
        }
      }
    } catch (error) {
      console.error(error);
      setIndicator(indicatorState.error);
      if (error instanceof Error) {
        setIndicatorText(error.message);
      } else {
        setIndicatorText(indicatorTextState.createdFail);
      }
    }
  };

  return (
    <div className="flex justify-center items-center h-screen">
      <form
        onSubmit={handleFormSubmit}
        className="flex flex-col justify-center items-center place-self-center rounded-lg bg-card-bg p-5 text-white"
      >
        <h1 className="text-3xl font-bold mb-3">Create a new account</h1>
        <InputField
          name="username"
          labelText="Username"
          placeholder="Username"
          type="text"
          grid
        />
        <InputField
          name="password"
          labelText="Password"
          placeholder="Password"
          type="password"
          grid
        />
        <InputField name="role" labelText="Role" select={["User", "Admin"]} grid />
        {indicator !== indicatorState.none && (
          <h3
            className={`text-xl ${
              indicator === indicatorState.success
                ? "text-green-500"
                : "text-red-500"
            }`}
          >
            {indicatorText}
          </h3>
        )}
        <div>
          <button
            className="bg-green-700 hover:bg-green-500 font-sans p-2 text-xl m-3 rounded-lg hover:scale-110 transition-all duration-300 cursor-pointer"
            type="submit"
          >
            Sign up
          </button>
          <Link
            href="/"
            className="inline-block bg-red-700 hover:bg-red-500 font-sans p-2 text-xl m-3 rounded-lg hover:scale-110 transition-all duration-300 select-none"
          >
            Go back
          </Link>
        </div>
      </form>
    </div>
  );
};

export default Signup;
