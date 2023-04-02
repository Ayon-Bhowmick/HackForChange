import { Button, View, Text, Alert } from "react-native"
import { useEffect } from "react"
import { useIsSignInWithProvider } from "../hooks/useSignInWithProvider"

export function Auth() {
    const { isLoading: isLoadingFacebook, error: errorFacebook, signIn: signInWithFacebook } = useIsSignInWithProvider('facebook')
    const { isLoading: isLoadingGoogle, error: errorGoogle, signIn: signInWithGoogle } = useIsSignInWithProvider('google')

    const isLoading = isLoadingFacebook || isLoadingGoogle
    const error = errorFacebook || errorGoogle

    useEffect( () => {
        if (error) Alert.alert('Error', error)
    }, [errorFacebook, errorGoogle])

    console.log({isLoading})

    return (
        <View>
            {/*<Button title="Sign in Google" onPress={() => signInWithGoogle() } disabled={isLoading}/>*/}
        </View>
    )
}