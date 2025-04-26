"use client";

import React, { useState, FC } from "react";
import InputField from "@components/InputField";
import Link from "next/link";
import { createUserAction } from "../../actions/users";
import { createLogAction } from "../../actions/logs";
import { useSession } from "next-auth/react";
import { Action, Severity } from "../../lib/enums";

interface SignupProps {
  initialRoleNames: string[];
}

const Signup: FC<SignupProps> = ({ initialRoleNames }) => {
  const roleNames: string[] = initialRoleNames;

  const { data: session } = useSession();

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

    const form = event.currentTarget;

    try {
      const formData = new FormData(event.currentTarget);
      const response = await createUserAction(formData);

      if (!response.success) throw new Error(response.error);

      setIndicator(indicatorState.success);
      setIndicatorText(response.success);
      if (session?.user.id) {
        await createLogAction({
          userId: session.user.id,
          roleId: session.user.roleId._id,
          action: Action.Create,
          severity: Severity.Medium,
          description: `${
            session.user.name
          } has created a new account for ${formData.get("username")}`,
          createdAt: new Date(),
        });
      }
      form.reset();
    } catch (error) {
      console.error(error);
      setIndicator(indicatorState.error);
      setIndicatorText(
        error instanceof Error ? error.message : indicatorTextState.createdFail
      );
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
        <InputField name="role" labelText="Role" select={roleNames} grid />
        {indicator !== indicatorState.none && (
          <h3
            className={`text-xl text-center whitespace-pre-line ${
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
