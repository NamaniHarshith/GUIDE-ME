// import 'package:dio/dio.dart';

// Future<String> apiReadText({required String path}) async {
//   print("API READ TEXT");
//   print(path);
//   var dio = Dio();
//   var formData = FormData();
//   formData.files.add(MapEntry(
//     "file",
//     await MultipartFile.fromFile(path, filename: "pic-name.png"),
//   ));
//   var response =
//       await dio.post('http://192.168.31.197:5000/detected_txt', data: formData);
//   print(response.data.toString());
//   return response.data.toString();
// }
import 'package:google_ml_kit/google_ml_kit.dart';

Future<String> extractTextFromImage({required String path}) async {
  final inputImage = InputImage.fromFilePath(path);
  final textRecognizer = GoogleMlKit.vision.textRecognizer(); 

  try {
    final RecognizedText recognizedText =
        await textRecognizer.processImage(inputImage);

    print("Extracted Text: ${recognizedText.text}");
    return recognizedText.text;
  } catch (e) {
    print("Error extracting text: $e");
    return 'Error extracting text: $e';
  } finally {
    textRecognizer.close();
  }
}
