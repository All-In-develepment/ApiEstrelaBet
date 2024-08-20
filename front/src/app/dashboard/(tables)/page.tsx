import { IGames, IReturn } from "@/app/models/Games";
import React from "react";

const LeagueTable = ({ league, datas }) => {
  const horas = [...new Set(datas.map((jogo) => jogo.hora))];
  const minutos = [...new Set(datas.map((jogo) => jogo.minuto))];

  return (
    <div className="overflow-x-auto">
      <h2 className="text-xl font-bold mb-4">{league}</h2>
      <table className="min-w-full bg-white">
        <thead>
          <tr>
            <th className="px-4 py-2">Hora/Minuto</th>
            {minutos.map((minuto) => (
              <th key={minuto} className="px-4 py-2">
                {minuto} min
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {horas.map((hora) => (
            <tr key={hora}>
              <td className="border px-4 py-2">{hora}h</td>
              {minutos.map((minuto) => {
                const jogo = datas.find(
                  (j) => j.hora === hora && j.minuto === minuto
                );
                return (
                  <td key={minuto} className="border px-4 py-2">
                    {jogo ? jogo.scoreboard : "-"}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

const LeagueTables = ({ retorno }: IGames) => {
  const leagues = Object.keys(retorno);

  return (
    <div className="grid grid-cols-1 gap-8">
      {leagues.map((league) => (
        <LeagueTable key={league} league={league} datas={retorno[league]} />
      ))}
    </div>
  );
};

export default LeagueTables;
