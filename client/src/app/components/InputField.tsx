import React, { FC } from "react";

interface IInputFieldProps {
  name: string;
  labelText?: string;
  select?: string[];
  grid?: boolean;
  defaultValue?: string;
  onChange?: (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => void;
  value?: string;
  placeholder?: string;
  type?: string;
}

const InputField: FC<IInputFieldProps> = ({
  name,
  labelText,
  select = [],
  grid = false,
  defaultValue,
  onChange,
  value,
  placeholder,
  type,
}) => {
  return (
    <div
      className={`${
        grid ? "grid grid-cols-2 w-72" : "flex"
      } justify-center text-lg items-center m-2`}
    >
      {labelText && (
        <label className="text-center block font-bold mr-2" htmlFor={name}>
          {labelText}
        </label>
      )}
      {select.length > 0 ? (
        <select
          className="bg-gray-700 select-none p-1 rounded-md hover:bg-gray-600 cursor-pointer transition-colors"
          name={name}
          defaultValue={defaultValue}
          onChange={onChange}
          value={value}
        >
          {select.map((item, index) => (
            <option key={index} value={item.toLowerCase()}>
              {item}
            </option>
          ))}
        </select>
      ) : (
        <input
          className="bg-gray-700 rounded-md"
          name={name}
          type={type}
          placeholder={placeholder}
          defaultValue={defaultValue}
          onChange={onChange}
          value={value}
        />
      )}
    </div>
  );
};

export default InputField;
