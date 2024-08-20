"use client";
import { useEffect, useState } from "react";
import axios from "axios";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from "@mui/material";
import { IGames, IReturn } from "../models/Games";

export default function Dashboard() {
  const [data, setData] = useState<{ [key: string]: IReturn[] } | undefined>(
    undefined
  );

  const fetchData = async () => {
    try {
      const { data } = await axios.get<IGames>(
        "https://www.plataforma.easycoanalytics.com.br/api-easy-analytics/api.php?action=getKironPartida"
      );

      const getLeague = data.retorno.reduce(
        (acc: { [key: string]: IReturn[] }, match) => {
          const { league } = match;

          if (!acc[league]) acc[league] = [];

          acc[league].push(match);

          return acc;
        },
        {}
      );

      setData(getLeague);
    } catch (error) {
      console.log("deu beibreyde", error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const leagueNames: { [key: string]: string } = {
    EnglishFastLeagueFootballSingleMatch: "Inglês",
    ItalianFastLeagueFootballSingleMatch: "Italiano",
    SpanishFastLeagueFootballSingleMatch: "Espanhol",
  };

  return (
    <div className="p-6 flex justify-center">
      <div className="w-full max-w-4xl">
        {data &&
          Object.keys(data).map((league) => (
            <TableComponent
              key={league}
              league={leagueNames[league] || league}
              matches={data[league]}
            />
          ))}
      </div>
    </div>
  );
}

const TableComponent = ({
  league,
  matches,
}: {
  league: string;
  matches: IReturn[];
}) => {
  // Organize matches by hour and minute
  const tableData: { [key: string]: { [key: number]: string } } = {};

  matches.forEach(({ hora, minuto, scoreboard }) => {
    if (!tableData[hora]) tableData[hora] = {};
    tableData[hora][minuto] = scoreboard;
  });

  const hours = Object.keys(tableData)
    .map(Number)
    .sort((a, b) => a - b);
  const minutes = Array.from(new Set(matches.map(({ minuto }) => minuto))).sort(
    (a, b) => a - b
  );

  return (
    <div className="mb-8">
      <h2 className="text-2xl font-bold mb-4">{league}</h2>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Hora</TableCell>
              {minutes.map((minute) => (
                <TableCell key={minute}>{minute}:00</TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {hours.map((hour) => (
              <TableRow key={hour}>
                <TableCell>{hour}</TableCell>
                {minutes.map((minute) => (
                  <TableCell key={`${hour}-${minute}`}>
                    {tableData[hour]?.[minute] || "-"}
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
};
