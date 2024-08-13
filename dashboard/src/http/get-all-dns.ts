// import { api } from "@/lib/api";
import { Dns } from "@/types/Dns";

export default async function getAllDns(): Promise<Dns[]> {
    //const { data } = await api.get<Dns[]>('/dns/all');
    return [
        {
            id: 1,
            nome: 'Vivo Fibra',
            ping: Math.floor(Math.random() * 101),
            checked_on: new Date()
        },
        {
            id: 2,
            nome: 'Vivo Pré',
            ping: Math.floor(Math.random() * 101),
            checked_on: new Date()
        },
        {
            id: 3,
            nome: 'Vivo Easy',
            ping: Math.floor(Math.random() * 101),
            checked_on: new Date()
        },
        {
            id: 4,
            nome: 'Vivo Controle',
            ping: Math.floor(Math.random() * 101),
            checked_on: new Date()
        },
        {
            id: 5,
            nome: 'Vivo Pós',
            ping: Math.floor(Math.random() * 101),
            checked_on: new Date()
        },
    ];
}