"use client";

import React, { FC } from "react";
import { dmDiscordUser } from "../actions/discord";
import PanelButton from "./PanelButton";
import { usePopupStore } from "../zustand/popupStore";
import BaseAction from "./BaseAction";

const KickButton: FC<{ userId: string }> = ({ userId }) => {
  const handleKick = () => {
    try {
      usePopupStore.setState({
        show: true,
        header: "Kick",
        text: (
          <BaseAction
            buttonText="Kick"
            mutationFn={(formData) => dmDiscordUser(userId, formData, "DELETE")}
          />
        ),
        isSubmit: true,
      });
    } catch (error) {
      console.error(error);
    }
  };

  return <PanelButton text="Kick" onClick={handleKick} />;
};

export default KickButton;
