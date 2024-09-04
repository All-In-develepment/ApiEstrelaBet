export interface IGames {
  retorno: IReturn[];
}

export interface IReturn {
  league: string;
  hour_match: string;
  data_match: string;
  team_home: string;
  team_visitor: string;
  scoreboard: string;
  hora: number;
  minuto: number;
}
