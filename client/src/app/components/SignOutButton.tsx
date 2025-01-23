"use client";

import { signOut } from "next-auth/react";
import React, { useState } from "react";
import Alert from "./Alert";

const SignOutButton = () => {
  const [alert, setAlert] = useState({
    show: false,
    text: "",
    onConfirm: () => {},
  });

  const resetAlert = () => {
    setAlert({ show: false, text: "", onConfirm: () => {} });
  };

  const handleSignOut = () => {
    try {
      setAlert({
        show: true,
        text: "Are you sure you want to sign out?",
        onConfirm: async () => {
          await signOut();
          resetAlert();
        },
      });
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <>
      <Alert
        text={alert.text}
        onConfirm={alert.onConfirm}
        onDismiss={() => resetAlert()}
        alert={alert}
      />
      <button
        className="bg-pink-900 mx-2 hover:bg-pink-500 hover:scale-110 transition-all duration-300 text-white font-bold py-2 px-4 rounded mt-4 cursor-pointer"
        onClick={() => handleSignOut()}
      >
        Sign out
      </button>
    </>
  );
};

export default SignOutButton;
