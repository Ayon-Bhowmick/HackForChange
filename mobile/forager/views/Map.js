import { Button, StyleSheet, Text, View } from 'react-native';

export default function Map({navigation}) {
  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
        <Text>Map Screen</Text>
        <Button
        title="Go to Pin"
        onPress={() => navigation.navigate('Pin')}
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
