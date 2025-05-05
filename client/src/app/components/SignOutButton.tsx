"use client";

import { signOut } from "next-auth/react";
import React from "react";
import { usePopupStore } from "../zustand/popupStore";
import SidebarButton from "./SidebarButton";
import { faSignOut } from "@fortawesome/free-solid-svg-icons";

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

  return <SidebarButton icon={faSignOut} text="Sign Out" onClick={handleSignOut} />;
};

export default SignOutButton;
