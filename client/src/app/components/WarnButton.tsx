import React, { FC, useState } from "react";
import PanelButton from "./PanelButton";
import PopupButton from "./PopupButton";
import { usePopupStore } from "../zustand/popupStore";
import { dmDiscordUser } from "../actions/discord";
import GearSpin from "./GearSpin";

interface IWarnProps {
  userId: string;
}

const FormWarn: FC<IWarnProps> = ({ userId }) => {
  const { onDismiss, resetPopup } = usePopupStore();

  const [loading, setLoading] = useState<boolean>(false);

  const handleFormSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setLoading(true);
    try {
      const formData = new FormData(event.target as HTMLFormElement);
      await dmDiscordUser(userId, formData);
      resetPopup();
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="flex flex-col flex-wrap" onSubmit={handleFormSubmit}>
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
            <PopupButton text="Warn" isSubmit={true} />
            <PopupButton text="Cancel" onClick={onDismiss} />
          </>
        )}
      </div>
    </form>
  );
};

const WarnButton: FC<IWarnProps> = ({ userId }) => {
  const handleWarn = () => {
    try {
      usePopupStore.setState({
        show: true,
        header: "Warn",
        text: <FormWarn userId={userId} />,
        isSubmit: true,
      });
    } catch (error) {
      console.error(error);
    }
  };

  return <PanelButton text="Warn" onClick={handleWarn} />;
};

export default WarnButton;
