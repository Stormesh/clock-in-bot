import React, { FC } from "react";
import PanelButton from "./PanelButton";
import { usePopupStore } from "../zustand/popupStore";
import { dmDiscordUser } from "../actions/discord";
import BaseAction from "./BaseAction";

const WarnButton: FC<{ userId: string }> = ({ userId }) => {
  const handleWarn = () => {
    try {
      usePopupStore.setState({
        show: true,
        header: "Warn",
        text: (
          <BaseAction
            buttonText="Warn"
            mutationFn={(formData) => dmDiscordUser(userId, formData)}
          />
        ),
        isSubmit: true,
      });
    } catch (error) {
      console.error(error);
    }
  };

  return <PanelButton text="Warn" onClick={handleWarn} />;
};

export default WarnButton;
