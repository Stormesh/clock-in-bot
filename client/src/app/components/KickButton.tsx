"use client";

import React, { FC, useState } from "react";
import PanelButton from "./PanelButton";
import PopupButton from "./PopupButton";
import { usePopupStore } from "../zustand/popupStore";
import { dmDiscordUser } from "../actions/actions";
import GearSpin from "./GearSpin";

interface IKickProps {
  userId: string;
}

const FormKick: FC<IKickProps> = ({ userId }) => {
  const { onDismiss, resetPopup } = usePopupStore();

  const [loading, setLoading] = useState<boolean>(false);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setLoading(true);
    try {
      const formData = new FormData(event.target as HTMLFormElement);
      await dmDiscordUser(userId, formData, "DELETE");
      resetPopup();
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="flex flex-col" onSubmit={handleSubmit}>
      <h3 className="text-center text-xl">Enter the reason</h3>
      <textarea
        className="bg-purple-100 text-black p-2 rounded-md m-2"
        name="message"
        placeholder="Reason"
      />
      <div className="flex justify-center items-center">
        {loading ? (
          <GearSpin />
        ) : (
          <>
            <PopupButton text="Kick" isSubmit={true} />
            <PopupButton text="Cancel" onClick={onDismiss} />
          </>
        )}
      </div>
    </form>
  );
}

const KickButton: FC<IKickProps> = ({ userId }) => {
  const handleKick = () => {
    try {
      usePopupStore.setState({
        show: true,
        header: "Kick",
        text: <FormKick userId={userId} />,
        isSubmit: true,
      });
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <>
      <PanelButton
        text="Kick"
        color="bg-red-900"
        hoverColor="hover:bg-red-500"
        onClick={handleKick}
      />
    </>
  );
};

export default KickButton;
