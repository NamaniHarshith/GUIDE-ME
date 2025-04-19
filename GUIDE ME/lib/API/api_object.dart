import 'package:dio/dio.dart';

Future<String> apiObject({required String path}) async {
  print("API OBJECT");
  print(path);

  var dio = Dio(
    BaseOptions(
      connectTimeout: const Duration(seconds: 10), // 🔧 Add a timeout
      receiveTimeout: const Duration(seconds: 15),
      sendTimeout: const Duration(seconds: 10),
    ),
  );

  var formData = FormData();
  formData.files.add(
    MapEntry(
      "file",
      await MultipartFile.fromFile(path, filename: "pic-name.png"),
    ),
  );

  try {
    var response = await dio.post(
      'http://192.168.60.73:5000/detected_obj',
      data: formData,
    );
    print(response.data.toString());
    return response.data.toString();
  } catch (e) {
    print("API call error: $e");
    return "Error: $e";
  }
}
