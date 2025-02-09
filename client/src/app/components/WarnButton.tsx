import React, { FC } from "react";
import PanelButton from "./PanelButton";
import PopupButton from "./PopupButton";
import { usePopupStore } from "../zustand/popupStore";
import { dmDiscordUser } from "../actions/actions";

interface IWarnButtonProps {
  userId: string;
}

const WarnButton: FC<IWarnButtonProps> = ({ userId }) => {
  const {
    onDismiss,
    resetPopup,
  } = usePopupStore();

  const warn = async (event: React.FormEvent) => {
    try {
      event.preventDefault();

      const formData = new FormData(event.target as HTMLFormElement);
      await dmDiscordUser(userId, formData);
      resetPopup();
    } catch (error) {
      console.error(error);
    }
  };

  const handleWarn = () => {
    try {
      usePopupStore.setState({
        show: true,
        header: "Warn",
        text: (
          <form className="flex flex-col flex-wrap" onSubmit={warn}>
            <h3 className="text-center text-xl">Enter the reason</h3>
            <textarea
              className="bg-purple-100 text-black p-2 rounded-md m-2"
              name="message"
              placeholder="Reason"
            />
            <div>
              <PopupButton text="Warn" isSubmit={true} />
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
        text="Warn"
        color="bg-amber-900"
        hoverColor="hover:bg-amber-500"
        onClick={handleWarn}
      />
    </>
  );
};

export default WarnButton;
