import { Button, View, Text, Alert } from "react-native"
import { useEffect } from "react"
import { useIsSignInWithProvider } from "../hooks/useSignInWithProvider"

export function Auth() {
    const { isLoading: isLoadingGoogle, error: errorGoogle, signIn: signInWithGoogle } = useIsSignInWithProvider('google')

    const isLoading = isLoadingGoogle
    const error = errorGoogle

    useEffect( () => {
        if (error) Alert.alert('Error', error)
    }, [errorGoogle])

    console.log({isLoading})

    return (
        <View>
            <Text>
                {'\n\n\n\n\n\n\n\n\n\n\n\n\n\n'}
                Login Page
            </Text>
            <Button title="Log in with Google" onPress={() => signInWithGoogle() } disabled={isLoading}/>
        </View>
    )
}