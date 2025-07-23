import React, { FC } from "react";
import PopupButton from "./PopupButton";
import { usePopupStore } from "../zustand/popupStore";
import GearSpin from "./GearSpin";
import { useMutation } from "@tanstack/react-query";

interface IBaseActionProps {
  buttonText: string;
  mutationFn: (formData: FormData) => Promise<void>;
}

const BaseAction: FC<IBaseActionProps> = ({ 
  buttonText, 
  mutationFn 
}) => {
  const { onDismiss, resetPopup } = usePopupStore();
  
  const mutation = useMutation({
    mutationFn: mutationFn,
    onSuccess: () => {
      resetPopup();
    },
    onError: (error) => {
      console.error(error);
    },
  });
  
  const handleFormSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    mutation.mutateAsync(new FormData(event.target as HTMLFormElement));
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
        {mutation.isPending ? (
          <GearSpin />
        ) : (
          <>
            <PopupButton text={buttonText} isSubmit={true} />
            <PopupButton text="Cancel" onClick={onDismiss} />
          </>
        )}
      </div>
    </form>
  );
};

export default BaseAction;