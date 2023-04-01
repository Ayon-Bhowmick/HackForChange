import { Button, StyleSheet, Text, View } from 'react-native';

export default function Login({navigation}) {
  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
        <Text>Login screen</Text>
        <Button
        title="Log in"
        onPress={() => navigation.navigate('Map')}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
