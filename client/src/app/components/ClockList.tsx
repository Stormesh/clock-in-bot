"use client";

import React, { useEffect, useRef, useState } from "react";
import ClockCard from "@components/ClockCard";
import ClockHeader from "@components/ClockHeader";
import { io, Socket } from "socket.io-client";

const DISCORD_BOT_URL = process.env.NEXT_PUBLIC_DISCORD_BOT_URL ?? "";

if (!DISCORD_BOT_URL) {
  console.error(
    "Please define the DISCORD_BOT_URL environment variable inside .env.local"
  );
}

const url = DISCORD_BOT_URL;

interface IUser {
  id: number;
  name: string;
  avatar: string;
  clockTime: number;
  meetingTime: number;
  breakTime: number;
  isClockedIn: boolean;
  onBreak: boolean;
  onMeeting: boolean;
}

const ClockList = () => {
  const [userData, setUserData] = useState<IUser[]>([]);
  const socket = useRef<Socket | null>(null);

  const updateTime = (userId: number) => {
    setUserData((prevUserData) =>
      prevUserData.map((user) =>
        user.id === userId
          ? {
              ...user,
              clockTime: user.isClockedIn ? user.clockTime + 1 : user.clockTime,
              breakTime: user.onBreak ? user.breakTime + 1 : user.breakTime,
              meetingTime: user.onMeeting
                ? user.meetingTime + 1
                : user.meetingTime,
            }
          : user
      )
    );
  };

  const getUserData = async () => {
    try {
      const response = await fetch(`${url}/api/users`);
      const data = await response.json();
      setUserData(data);
    } catch (error) {
      console.error("Error fetching user data: ", error);
    }
  };

  useEffect(() => {
    if (!url) return;
    socket.current = io(url);
    socket.current.on("update", getUserData);

    return () => {
      socket.current?.disconnect();
    };
  });

  useEffect(() => {
    getUserData();

    const updateTimeOnVisibilityChange = () => {
      if (document.visibilityState === "visible") {
        getUserData();
      }
    };

    document.addEventListener("visibilitychange", updateTimeOnVisibilityChange);

    return () => {
      document.removeEventListener(
        "visibilitychange",
        updateTimeOnVisibilityChange
      );
    };
  }, []);

  useEffect(() => {
    const timeInterval = setInterval(() => {
      userData.forEach((user) => {
        if (user.isClockedIn || user.onBreak || user.onMeeting) {
          updateTime(user.id);
        }
      });
    }, 1000);

    return () => {
      clearInterval(timeInterval);
    };
  }, [userData]);

  return (
    <>
      {userData.length > 0 ? (
        <table className="text-3xl mt-10 mx-auto table border-2 border-collapse shadow-sm shadow-black">
          <ClockHeader />
          <tbody className="text-center border-2 border-[#453c8a]">
            {userData.map((user) => {
              return (
                <ClockCard
                  key={user.id}
                  name={user.name}
                  avatar={user.avatar}
                  clockTime={user.clockTime}
                  meetingTime={user.meetingTime}
                  breakTime={user.breakTime}
                  isClockedIn={user.isClockedIn}
                  onBreak={user.onBreak}
                  onMeeting={user.onMeeting}
                />
              );
            })}
          </tbody>
        </table>
      ) : (
        <h2 className="text-center text-5xl text-white font-sans mt-[25rem]">
          No one is clocked in yet.
        </h2>
      )}
    </>
  );
};

export default ClockList;
