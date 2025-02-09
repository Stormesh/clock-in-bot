import React, { FC } from "react";
import PanelButton from "./PanelButton";
import PopupButton from "./PopupButton";
import { usePopupStore } from "../zustand/popupStore";
import { dmDiscordUser } from "../actions/actions";

interface IKickButtonProps {
  userId: string;
}

const KickButton: FC<IKickButtonProps> = ({ userId }) => {
  const {
    onDismiss,
    resetPopup,
  } = usePopupStore();

  const kick = async (event: React.FormEvent) => {
    try {
      event.preventDefault();

      const formData = new FormData(event.target as HTMLFormElement);
      await dmDiscordUser(userId, formData, "DELETE");
      resetPopup();
    } catch (error) {
      console.error(error);
    }
  };

  const handleKick = () => {
    try {
      usePopupStore.setState({
        show: true,
        header: "Kick",
        text: (
          <form className="flex flex-col flex-wrap" onSubmit={kick}>
            <h3 className="text-center text-xl">Enter the reason</h3>
            <textarea
              className="bg-purple-100 text-black p-2 rounded-md m-2"
              name="message"
              placeholder="Reason"
            />
            <div>
              <PopupButton text="Kick" isSubmit={true} />
              <PopupButton text="Cancel" onClick={onDismiss} />
            </div>
          </form>
        ),
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
