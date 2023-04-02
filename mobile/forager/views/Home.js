import { useEffect, useState } from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';
import { supabase } from '../services/supabase';

export function Home() {
    const [user, setUser] = useState({
        name: "Loading...",
        email: "Loading...",
        phone: "Loading..."
    })

    const signout = async () => {
        const { error } = await supabase.auth.signOut()
        if(error) return console.log(error)
    }

    useEffect(() => {
        supabase.auth.getSession()
        .then(({ data, error }) => {
            const { phone, user_metadata } = data.session.user
            const { full_name: name, email } = user_metadata
            setUser({name, email, phone}) 
        })
    }, [])

    return (
        <View>
            <Text>Bienvenido a mi app</Text>
            <Text>Bienvenido a mi app</Text>
            <Text>Bienvenido a mi app</Text>
            <Text>Name: {user.name}</Text>
            <Text>Email: {user.email}</Text>
            <Text>Phone: {user.phone}</Text>
            <Button title='Cerrar' onPress={() => signout()}/>
        </View>
    )
}