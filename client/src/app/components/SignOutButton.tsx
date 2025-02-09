"use client";

import { signOut } from "next-auth/react";
import React from "react";
import { usePopupStore } from "../zustand/popupStore";
import PanelButton from "./PanelButton";

const SignOutButton = () => {
  const { resetPopup } = usePopupStore();

  const handleSignOut = () => {
    try {
      usePopupStore.setState({
        show: true,
        text: "Are you sure you want to sign out?",
        onConfirm: async () => {
          await signOut();
          resetPopup();
        },
        onDismiss: resetPopup,
      });
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <>
      <PanelButton text="Sign Out" color="bg-pink-900" hoverColor="hover:bg-pink-500" onClick={handleSignOut} />
    </>
  );
};

export default SignOutButton;
