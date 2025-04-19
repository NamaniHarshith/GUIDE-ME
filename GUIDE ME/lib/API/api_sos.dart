import 'package:dio/dio.dart';

Future<void> apiSOS() async {
  print("API SOS");

  var dio = Dio(
    BaseOptions(
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 15),
      sendTimeout: const Duration(seconds: 10),
    ),
  );

  try {
    final response = await dio.post(
      // "http://liraj.pythonanywhere.com/sos", // Live URL (uncomment when needed)
      "http://192.168.60.73:5000/sos",
      data: {
        'data': ["9391405049"],
      },
    );
    print("SOS Response: ${response.data}");
  } on DioException catch (dioError) {
    print("Dio error: ${dioError.message}");
  } catch (e) {
    print("Unexpected error: $e");
  }
}
