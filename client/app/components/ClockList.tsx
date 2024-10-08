"use client";

import React, { FC, useEffect, useState } from "react";
import styles from "@/styles/clock.module.css";
import ClockCard from "./ClockCard";
import ClockHeader from "./ClockHeader";
import { io } from "socket.io-client";

const url = "http://localhost:5000";
const socket = io(url);

interface User {
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

const ClockList: FC = () => {
  const [userData, setUserData] = useState<User[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  
  useEffect(() => {
    const getUserData = async () => {
      try {
        const response = await fetch(`${url}/api/users`, {
          cache: "no-cache",
        });
        const data = await response.json();
        setUserData(data);
      } catch (error) {
        console.error("Error fetching user data: ", error);
      } finally {
        setLoading(false);
      }
    };

    getUserData();

    socket.on('update', (message) => {
      console.log('Message from server: ', message);
      getUserData();
    });

    return () => {
      socket.off('update')
    };
  }, []);

  if (loading) {
    return <h2 className={styles.loadingClock}>Loading...</h2>;
  }

  return (
    <>
      {userData.length > 0 ? (
        <table className={styles.clockTable}>
          <ClockHeader />
          <tbody>
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
        <h2 className={styles.noData}>No one is clocked in yet.</h2>
      )}
    </>
  );
};

export default ClockList;
