import React, { FC } from "react";
import Image from "next/image";
import styles from "@/styles/clock.module.css";
import WarnButton from "./WarnButton";
import KickButton from "./KickButton";
import { Permissions } from "../lib/enums";
import { useSession } from "next-auth/react";

interface IUserProps {
  id: string;
  name: string;
  avatar: string;
  clockTime: number;
  meetingTime: number;
  breakTime: number;
  isClockedIn: boolean;
  onBreak: boolean;
  onMeeting: boolean;
}

const ClockCard: FC<IUserProps> = ({
  id,
  name,
  avatar,
  clockTime,
  meetingTime,
  breakTime,
  isClockedIn,
  onBreak,
  onMeeting,
}) => {
  const { data: session } = useSession();

  const canKickOrWarn = session?.user.roleId.permissions?.some(
    (permission) =>
      permission === Permissions.Kick || permission === Permissions.Warn
  );

  const setZeros = (num: number) => {
    return num < 10 ? `0${num}` : num;
  };

  const timeFormat = (time: number) => {
    const hours = Math.floor(time / 3600);
    const minutes = Math.floor((time % 3600) / 60);
    const seconds = time % 60;
    return `${setZeros(hours)}:${setZeros(minutes)}:${setZeros(seconds)}`;
  };

  const timeElement = (time: number, effect: boolean, emoji: string) => {
    return (
      <td className="text-violet-200 font-mono">
        {timeFormat(time)}
        <span
          className={
            effect
              ? `${styles.onEffect} inline-block text-xl md:text-4xl md:pl-2`
              : "hidden"
          }
          aria-hidden={!effect}
        >
          {emoji}
        </span>
      </td>
    );
  };

  return (
    <>
      <tr
        className={`border-2 ${
          canKickOrWarn && "border-b-transparent"
        } text-lg md:text-3xl`}
      >
        <td>
          <div className="mx-2 md:mx-3 my-1 flex flex-col items-center justify-center">
            <Image
              className="rounded-full m-1 hover:scale-110 transition-transform w-[65px] h-[65px] md:w-[100px] md:h-[100px]"
              src={avatar}
              alt={name}
              width={100}
              height={100}
            />
            <p className="text-violet-300 font-sans font-light">{name}</p>
          </div>
        </td>
        {timeElement(clockTime, isClockedIn, "🕒")}
        {timeElement(meetingTime, onMeeting, "📅")}
        {timeElement(breakTime, onBreak, "☕")}
      </tr>
      {canKickOrWarn && (
        <tr>
          <td colSpan={4}>
            <div className="flex items-center justify-center">
              <div className="bg-linear-to-t p-2 from-card-bg to-table-border rounded-t-full w-1/2">
                {session?.user.roleId.permissions?.includes(
                  Permissions.Warn
                ) && <WarnButton userId={id} />}
                {session?.user.roleId.permissions?.includes(
                  Permissions.Kick
                ) && <KickButton userId={id} />}
              </div>
            </div>
          </td>
        </tr>
      )}
    </>
  );
};

export default ClockCard;
